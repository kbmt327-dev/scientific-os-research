import { ContentBody } from "@quartz-community/content-page"

/**
 * Authored index.md files are curated pages, not file-browser views. The stock
 * FolderPage remains enabled for virtual indexes where a listing is useful.
 */
export default function CuratedFolderPage() {
  return {
    name: "CuratedFolderPage",
    priority: 20,
    match: ({ slug, fileData }) =>
      slug.endsWith("/index") &&
      fileData?.relativePath?.replaceAll("\\", "/").endsWith("/index.md") === true,
    layout: "folder",
    body: ContentBody,
  }
}
