from django.urls import path

from .views import (
    ContractsList, ContractsCreate, ContractsUpdate, ContractsDelete, ContractsSearch,
    ProceedingsList, ProceedingsCreate, ProceedingsUpdate, ProceedingsDelete, ProceedingsSearch,
    AgreementsList, AgreementsCreate, AgreementsUpdate, AgreementsDelete, AgreementsSearch,
    BankReceiptsList, BankReceiptsCreate, BankReceiptsUpdate, BankReceiptsDelete, BankReceiptsSearch,
    ConditionStatementsList, ConditionStatementsCreate, ConditionStatementsUpdate, ConditionStatementsDelete, ConditionStatementsSearch,
    RegisteredDocsList, RegisteredDocsCreate, RegisteredDocsUpdate, RegisteredDocsDelete, RegisteredDocsSearch,
    OfficialDocsList, OfficialDocsCreate, OfficialDocsUpdate, OfficialDocsDelete, OfficialDocsSearch
)



app_name = 'projects_docs'


urlpatterns = [
    path('contracts/', ContractsList.as_view(), name='contracts'),
    path('contracts/search', ContractsSearch.as_view(), name='contracts_search'),
    path('contracts/create', ContractsCreate.as_view(), name='contract_create'),
    path('contracts/update/<int:pk>', ContractsUpdate.as_view(), name='contract_update'),
    path('contracts/delete/<int:pk>', ContractsDelete.as_view(), name='contract_delete'),

    path('proceedings/', ProceedingsList.as_view(), name='proceedings'),
    path('proceedings/search', ProceedingsSearch.as_view(), name='proceedings_search'),
    path('proceedings/create', ProceedingsCreate.as_view(), name='proceeding_create'),
    path('proceedings/update/<int:pk>', ProceedingsUpdate.as_view(), name='proceeding_update'),
    path('proceedings/delete/<int:pk>', ProceedingsDelete.as_view(), name='proceeding_delete'),

    path('agreements/', AgreementsList.as_view(), name='agreements'),
    path('agreements/search', AgreementsSearch.as_view(), name='agreements_search'),
    path('agreements/create', AgreementsCreate.as_view(), name='agreement_create'),
    path('agreements/update/<int:pk>', AgreementsUpdate.as_view(), name='agreement_update'),
    path('agreements/delete/<int:pk>', AgreementsDelete.as_view(), name='agreement_delete'),

    path('bank_receipts/', BankReceiptsList.as_view(), name='bank_receipts'),
    path('bank_receipts/search', BankReceiptsSearch.as_view(), name='bank_receipts_search'),
    path('bank_receipts/create', BankReceiptsCreate.as_view(), name='bank_receipt_create'),
    path('bank_receipts/update/<int:pk>', BankReceiptsUpdate.as_view(), name='bank_receipt_update'),
    path('bank_receipts/delete/<int:pk>', BankReceiptsDelete.as_view(), name='bank_receipt_delete'),

    path('condition_statements/', ConditionStatementsList.as_view(), name='condition_statements'),
    path('condition_statements/search', ConditionStatementsSearch.as_view(), name='condition_statements_search'),
    path('condition_statements/create', ConditionStatementsCreate.as_view(), name='condition_statement_create'),
    path('condition_statements/update/<int:pk>', ConditionStatementsUpdate.as_view(), name='condition_statement_update'),
    path('condition_statements/delete/<int:pk>', ConditionStatementsDelete.as_view(), name='condition_statement_delete'),

    path('registered_docs/', RegisteredDocsList.as_view(), name='registered_docs'),
    path('registered_docs/search', RegisteredDocsSearch.as_view(), name='registered_docs_search'),
    path('registered_docs/create', RegisteredDocsCreate.as_view(), name='registered_doc_create'),
    path('registered_docs/update/<int:pk>', RegisteredDocsUpdate.as_view(), name='registered_doc_update'),
    path('registered_docs/delete/<int:pk>', RegisteredDocsDelete.as_view(), name='registered_doc_delete'),

    path('official_docs/', OfficialDocsList.as_view(), name='official_docs'),
    path('official_docs/search', OfficialDocsSearch.as_view(), name='official_docs_search'),
    path('official_docs/create', OfficialDocsCreate.as_view(), name='official_doc_create'),
    path('official_docs/update/<int:pk>', OfficialDocsUpdate.as_view(), name='official_doc_update'),
    path('official_docs/delete/<int:pk>', OfficialDocsDelete.as_view(), name='official_doc_delete'),
]




