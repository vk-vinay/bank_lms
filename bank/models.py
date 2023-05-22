from django.db import models, transaction
from django.db.models import Sum

from bank import errors

# Create your models here.


class BankUser(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    @classmethod
    def create_user(cls, name):
        return cls.objects.create(name=name)

    @property
    def accounts(self):
        return self.account_set.all()


class Account(models.Model):
    user = models.ForeignKey(BankUser, on_delete=models.PROTECT)
    balance = models.FloatField(null=False, blank=False, default=0)

    @classmethod
    def create_account(cls, user):
        return cls.objects.create(user=user)

    @property
    def transaction(self):
        return self.transaction_set.all()
    @property
    def ledger(self):
        leger = self.transaction.annotate(balance=Sum('credit') - Sum('debit')).aggregate(Sum('balance'))
        return {
            "ledger_balance": None,
            "lrger": leger
        }


    @classmethod
    def deposit(cls, account, amount):
        if not amount > 0:
            raise errors.InvalidAmount(amount)
        try:
            with transaction.atomic():
                account = cls.objects.select_for_update().get(id=account)
                account.balance += amount
                account.transaction_set.create(credit=amount)
                account.save()
            return True
        except Exception as e:
            raise e

    @classmethod
    def withdraw(cls, account, amount):
        try:
            with transaction.atomic():
                account = cls.objects.select_for_update().get(id=account)
                if account.balance < amount:
                    raise errors.InsufficientFunds()
                account.balance -= amount
                account.transaction_set.create(debit=amount)
                account.save()
                return True
        except Exception as e:
            raise e

    @classmethod
    def transfer(cls, ac_from, ac_to, amount):
        if ac_from == ac_to:
            raise errors.SameAccount()

        try:
            with transaction.atomic():
                ac_from = cls.objects.select_for_update().get(id=ac_from)
                ac_to = cls.objects.select_for_update().get(id=ac_to)
                if ac_from.balance < amount:
                    raise errors.InsufficientFunds(ac_from.balance, amount)
                ac_from.balance -= amount
                ac_from.transaction_set.create(debit=amount)
                ac_to.balance += amount
                ac_to.transaction_set.create(credit=amount)
                ac_from.save()
                ac_to.save()
                return True
        except Exception as e:
            raise e


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    credit = models.FloatField(null=False, blank=False, default=0)
    debit = models.FloatField(null=False, blank=False, default=0)
