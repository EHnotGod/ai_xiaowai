<template><RouterView /></template>

<style>
:root { font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; color: #334155; }
body { margin: 0; min-width: 320px; background: linear-gradient(to bottom left, #b3dfe5, #f8fafc 75%); background-attachment: fixed; }
button, input, textarea { font-family: inherit; }
.markdown-content { line-height: 1.75; overflow-wrap: anywhere; }
.markdown-content > :first-child { margin-top: 0; }
.markdown-content > :last-child { margin-bottom: 0; }
.markdown-content img { max-width: 100%; height: auto; }
.markdown-content pre { max-width: 100%; overflow-x: auto; background: #f5f7fa; border-radius: 8px; padding: 12px; }
.markdown-content code { font-family: ui-monospace, Consolas, monospace; font-size: .9em; }
.markdown-content table { display: block; overflow-x: auto; border-collapse: collapse; }
.markdown-content td, .markdown-content th { border: 1px solid #d8e0eb; padding: 6px 10px; }
.markdown-content a { color: #3164c3; }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important; scroll-behavior: auto !important; } }
</style>
