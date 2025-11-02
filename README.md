### iOS Packager

To package and sign iOS application run:

```
./main.py application.app [cert] [bundle id postfix] [bundle name]? [executable name]?
```

- `cert` is `[bundle namespace];[team];[name]` (eg `adrian;ABC345;Apple Development: xyz@abc.com (XYZ123)`)
- resulting bundle will have ID `com.[bundle namespace].[bundle id postfix]`
