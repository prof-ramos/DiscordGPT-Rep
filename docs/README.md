# Documentation Shortcodes and UI Shims

This docs site uses a few lightweight shortcodes to keep content portable and Hugo builds deterministic. They are theme-agnostic shims designed to work with PaperMod.

## Tabs

Usage:

```
{{< tabs name="example-tabs" >}}
{{% tab name="🐳 Docker" %}}
Conteúdo para Docker.
{{% /tab %}}
{{% tab name="🐍 Python" %}}
Conteúdo para Python.
{{% /tab %}}
{{< /tabs >}}
```

- Params: `name` (string, optional; used to scope IDs). Child `tab` accepts `name` (or `title`).
- Behavior: Renders simple blocks; JS builds the tablist with keyboard navigation and ARIA.

## Cards

```
{{< cardpane >}}
{{< card header="**Título**" >}}Conteúdo do card{{< /card >}}
{{< card header="Outro" >}}Outro conteúdo{{< /card >}}
{{< /cardpane >}}
```

- Params: `header` (markdown enabled). Card items render directly inside a responsive grid.

## Alerts

```
{{< alert title="🎉 Pronto!" color="success" >}}
Mensagem de sucesso.
{{< /alert >}}
```

- Params: `title` (string), `color` (`info`, `success`, `warning`, `danger`).

## Blocks (compat)

Hero/sections/features used on the homepage:

```
{{< blocks/cover title="Titulo" color="primary" height="min" >}}
Conteúdo opcional
{{< /blocks/cover >}}

{{% blocks/lead color="white" %}}Texto em destaque{{% /blocks/lead %}}

{{% blocks/section color="primary" type="row" %}}
{{% blocks/feature icon="fas fa-robot" title="Recurso" %}}Descrição{{% /blocks/feature %}}
{{% /blocks/section %}}
```

- `blocks/cover`: Params `title`, `color`, `height`, `image_anchor`.
- `blocks/lead`: Param `color`.
- `blocks/section`: Params `color`, `type` (`row`|`stack`).
- `blocks/feature`: Params `icon`, `title`, `url`.
- `blocks/link-down`: Visual hint to scroll (no params required; optional `color`).

## Accessibility and Styling

- Tabs implement ARIA roles (`tablist`, `tab`, `tabpanel`) and keyboard: Left/Right, Home/End, Enter/Space.
- CSS uses PaperMod tokens: `--primary`, `--border`, `--entry`, `--tertiary`. Minimal overrides only.

## CI and Build

- GitHub Actions pins Hugo extended to `0.149.0` for consistent builds.
- Local build: `cd docs && hugo --minify`. Preview: `hugo server`.

