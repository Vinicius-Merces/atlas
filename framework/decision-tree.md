# Decision Tree

```text
Is the request clear?
├─ No → resolve using project context
└─ Yes
   ↓
Does an existing solution already exist?
├─ Yes → reuse or adapt
└─ No
   ↓
Does the change affect contracts or data?
├─ Yes → create plan, migration strategy, and review gate
└─ No
   ↓
Is the change reversible?
├─ No → require stronger evidence and approval
└─ Yes
   ↓
Implement the smallest coherent solution
   ↓
Validate all affected quality dimensions
   ↓
Document and deliver
```
