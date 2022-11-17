from django.contrib import admin
from web.models import Account , AccountLog ,AccountGroup , AccountGroupLog , AccountLedger ,AccountLedgerLog
#acount group

class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ('AccountGroupName','ParentGroup','Description')
admin.site.register(AccountGroup,AccountGroupAdmin)


class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ('AccountGroupName','ParentGroup','Description')
admin.site.register(AccountGroupLog,AccountGroupAdmin)
#account ledger


class AccountLedgerAdmin(admin.ModelAdmin):
    list_display = ('LedgerName','ParentGroup','OpeningBalanceType','OpeningBalanceAmount','Description')
admin.site.register(AccountLedger,AccountLedgerAdmin)


class AccountLedgerAdmin(admin.ModelAdmin):
    list_display = ('LedgerName','ParentGroup','OpeningBalanceType','OpeningBalanceAmount','Description')
admin.site.register(AccountLedgerLog,AccountLedgerAdmin)



