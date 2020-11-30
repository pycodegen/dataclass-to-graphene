# type conversion codegen:

generates code for

original-type <=> graphene-type

eg.

```python
# graphene_generated.types.User
import types.User

class User(graphene.Object):
    name = graphene.Field(...)
    ...

    # generated by `from_original_obj`
    @classmethod
    def _from_original(cls, original: types.User):
        ...

    # generated by `to_original_obj`
    classmethod
    def _to_original(cls, o: User):
        ...
```