def GlueETLJob(glueContext, args):
    datasource0 = glueContext.create_dynamic_frame.from_catalog(database=args['database'], table_name=args['table_name'])
    transformed = Filter.apply(frame=datasource0, f=lambda x: x["feedback_column"] is not None)
    glueContext.write_dynamic_frame.from_catalog(frame=transformed, database=args['redshift_database'], table_name=args['redshift_table_name'])
