from pathlib import Path
from codegen.Codegen import Codegen
from codegen.ModulePath import ModulePath
from codegen.ModulePath.RootModulePath import RootModulePath
from sample.graphql.AppContext import SampleAppContext
from sample.graphql.user_query import User


source_path = Path(__file__).resolve()
write_dir = source_path.parent.parent

print(write_dir)
#
codegen = Codegen(
    context_cls=SampleAppContext,
    root_module_path=RootModulePath(ModulePath('sample_graphql_generated')),
)
#
codegen.add_query(User)

codegen.process()

if __name__ == '__main__':
    print('write_dir: ', write_dir)
    codegen.write_files(root_folder=write_dir)
