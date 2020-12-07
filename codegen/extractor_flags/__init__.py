from codegen.extractor_flags.__base__ import BaseTempExtractorFlag

is_query_flag = BaseTempExtractorFlag('is_query')
is_mutation_flag = BaseTempExtractorFlag('is_mutation')
is_subscription_flag = BaseTempExtractorFlag('is_subscription')

is_context_cls_flag = BaseTempExtractorFlag('is_context_cls')