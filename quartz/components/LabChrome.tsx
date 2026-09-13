import { QuartzComponentProps } from "./types"

const repository = "https://github.com/kbmt327-dev/scientific-os-research"

function pageBase({ cfg, ctx }: QuartzComponentProps): string {
  if (ctx.argv.serve || !cfg.baseUrl) return ""
  return new URL(`https://${cfg.baseUrl}`).pathname.replace(/\/$/, "")
}

function route(base: string, slug: string): string {
  return `${base}/${slug.replace(/^\//, "").replace(/\/$/, "")}/`
}

function languageFor({ fileData }: QuartzComponentProps): "ja" | "en" {
  return fileData.frontmatter?.lang === "ja" ? "ja" : "en"
}

function counterpartSlug(slug: string, target: "ja" | "en"): string {
  const canonical = slug === "index" ? "" : slug.endsWith("/index") ? slug.slice(0, -6) : slug
  if (!canonical || canonical === "ja" || canonical === "en") return target
  if (canonical.startsWith("ja/") || canonical.startsWith("en/")) {
    return `${target}/${canonical.slice(3)}`
  }
  return target
}

export function LabHeader(props: QuartzComponentProps) {
  const base = pageBase(props)
  const lang = languageFor(props)
  const slug = String(props.fileData.slug ?? "index")

  return (
    <header class="lab-header">
      <a class="lab-skip-link" href="#lab-main-content">
        {lang === "ja" ? "本文へ移動" : "Skip to content"}
      </a>
      <a class="lab-brand" href={route(base, lang)}>
        Open Research Lab
      </a>
      <nav class="lab-language" aria-label={lang === "ja" ? "言語" : "Language"}>
        <a
          href={route(base, counterpartSlug(slug, "ja"))}
          lang="ja"
          data-language-choice="ja"
          aria-current={lang === "ja" ? "page" : undefined}
        >
          日本語
        </a>
        <span aria-hidden="true">/</span>
        <a
          href={route(base, counterpartSlug(slug, "en"))}
          lang="en"
          data-language-choice="en"
          aria-current={lang === "en" ? "page" : undefined}
        >
          EN
        </a>
      </nav>
    </header>
  )
}

export function LabSidebar(props: QuartzComponentProps) {
  const base = pageBase(props)
  const lang = languageFor(props)
  const ja = lang === "ja"
  const slug = String(props.fileData.slug ?? "")
  const canonical = slug.endsWith("/index") ? slug.slice(0, -6) : slug
  const current = (segment: string) => {
    if (segment === "") return canonical === lang
    return canonical === `${lang}/${segment}` || canonical.startsWith(`${lang}/${segment}/`)
  }
  const items = [
    ["", ja ? "トップ" : "Home"],
    ["research", ja ? "研究一覧" : "Research"],
    ["how-to-read", ja ? "Research Noteの読み方" : "How to read a Research Note"],
    ["about/open-research-lab", ja ? "このLabと運営者" : "About the lab and its builder"],
    ["contribute", ja ? "再現・反証・共同研究" : "Reproduce, challenge, collaborate"],
  ]

  return (
    <div class="lab-sidebar-shell">
      <button
        type="button"
        class="lab-sidebar-toggle"
        aria-controls="lab-sidebar-panel"
        aria-expanded="true"
      >
        <span class="lab-menu-icon" aria-hidden="true">
          <i></i>
          <i></i>
          <i></i>
        </span>
        <span class="lab-toggle-label">{ja ? "メニュー" : "Menu"}</span>
      </button>
      <div id="lab-sidebar-panel" class="lab-sidebar-panel">
        <nav class="lab-primary-nav" aria-label={ja ? "メインメニュー" : "Main menu"}>
          {items.map(([path, label]) => (
            <a
              href={route(base, path ? `${lang}/${path}` : lang)}
              aria-current={current(path) ? "page" : undefined}
            >
              {label}
            </a>
          ))}
          <a href={repository} class="external">
            GitHub <span aria-hidden="true">↗</span>
          </a>
        </nav>
      </div>
    </div>
  )
}

export function LabFooter() {
  return (
    <footer class="lab-footer">
      <span>© 2026 kbmt327</span>
      <small>
        Powered by <a href="https://quartz.jzhao.xyz/">Quartz</a>
      </small>
    </footer>
  )
}

export const labChromeScript = String.raw`
(() => {
  const storageKey = "orl-sidebar-collapsed"
  const languageKey = "orl-language"

  function setSidebarState() {
    const root = document.getElementById("quartz-root")
    const toggle = document.querySelector(".lab-sidebar-toggle")
    if (!root || !(toggle instanceof HTMLButtonElement)) return

    const mobile = window.matchMedia("(max-width: 800px)").matches
    let collapsed = mobile
    if (!mobile) {
      try { collapsed = window.localStorage.getItem(storageKey) === "true" } catch {}
    }
    root.classList.toggle("lab-sidebar-collapsed", !mobile && collapsed)
    root.classList.toggle("lab-sidebar-open", mobile && !collapsed)
    toggle.setAttribute("aria-expanded", String(!collapsed))

    if (toggle.dataset.labBound !== "true") {
      toggle.dataset.labBound = "true"
      toggle.addEventListener("click", () => {
        const isMobile = window.matchMedia("(max-width: 800px)").matches
        const isCollapsed = isMobile
          ? !root.classList.contains("lab-sidebar-open")
          : root.classList.contains("lab-sidebar-collapsed")
        const nextCollapsed = !isCollapsed
        root.classList.toggle("lab-sidebar-collapsed", !isMobile && nextCollapsed)
        root.classList.toggle("lab-sidebar-open", isMobile && !nextCollapsed)
        toggle.setAttribute("aria-expanded", String(!nextCollapsed))
        if (!isMobile) {
          try { window.localStorage.setItem(storageKey, String(nextCollapsed)) } catch {}
        }
      })
    }
  }

  if (!window.__openResearchLabChromeBound) {
    window.__openResearchLabChromeBound = true
    document.addEventListener("click", (event) => {
      const target = event.target instanceof Element ? event.target.closest("[data-language-choice]") : null
      const choice = target?.getAttribute("data-language-choice")
      if (choice === "ja" || choice === "en") {
        try { window.localStorage.setItem(languageKey, choice) } catch {}
      }
    })
    window.addEventListener("resize", setSidebarState)
    document.addEventListener("nav", setSidebarState)
  }
  setSidebarState()
})()
`
