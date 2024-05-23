import great_expectations as gx
from great_expectations.checkpoint import Checkpoint
import settings as credentials

context = gx.get_context()

'''
Connect to data
'''

CONNECTION_STRING = (f"mssql+pyodbc://{credentials.USERID}:{credentials.PASSWORD}"
                     f"@localhost/AdventureWorks2012?driver=ODBC+Driver+17+for+SQL+Server")

'''
Create datasource
'''

sql_datasource = context.sources.add_sql(
    name="sql_datasource_prod4", connection_string=CONNECTION_STRING
)

'''
Create DataAsset
'''

sql_datasource.add_table_asset(
    name="sql_product_data", schema_name="Production", table_name="Product"
)

batch_request = sql_datasource.get_asset("sql_product_data").build_batch_request()

'''
Create Expectations
'''

expectation_suite_name = "product_table_expectation_suite"
context.add_or_update_expectation_suite(expectation_suite_name=expectation_suite_name)
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=expectation_suite_name,
)
print(validator.head())

expected_avg_weight = 74.069219
expected_class_values = ["H", "M", "L"]
expected_color_values = ["Black",
                         "Blue",
                         "Grey",
                         "Multi",
                         "Red",
                         "Silver",
                         "Silver/Black",
                         "White",
                         "Yellow"]
validator.expect_column_values_to_be_unique(column="ProductID")
validator.expect_column_values_to_not_be_null(column="Name")
validator.expect_column_values_to_be_in_set(
    "Class", value_set=expected_class_values)
validator.expect_column_values_to_be_of_type("ListPrice", "MONEY")
validator.expect_column_values_to_not_be_null(column="DaysToManufacture")
validator.expect_column_values_to_be_between("DaysToManufacture", min_value=0, max_value=7)
validator.expect_column_mean_to_be_between("Weight", min_value=expected_avg_weight)
validator.expect_column_values_to_be_in_set(
    "Color", value_set=expected_color_values)


'''
Save Expectations Suite
'''

validator.save_expectation_suite(discard_failed_expectations=False)

'''
Validate Data
'''

my_checkpoint_name = "my_sql_checkpoint"

checkpoint = Checkpoint(
    name=my_checkpoint_name,
    run_name_template="%Y%m%d-%H%M%S-Production.Product-tests-run",
    data_context=context,
    batch_request=batch_request,
    expectation_suite_name=expectation_suite_name,
    action_list=[
        {
            "name": "store_validation_result",
            "action": {"class_name": "StoreValidationResultAction"},
        },
        {"name": "update_data_docs", "action": {"class_name": "UpdateDataDocsAction"}},
    ],
)

context.add_or_update_checkpoint(checkpoint=checkpoint)
checkpoint_result = checkpoint.run()

'''
Build and view Data Docs
'''

context.open_data_docs()
