# Helpjuice to Mintlify migration report

Generated 2026-09-22 from the `snagr-*-2026-09-22.csv` export.

## Summary

| Item | Count |
|---|---|
| Published articles migrated | 971 |
| &nbsp;&nbsp;en | 241 |
| &nbsp;&nbsp;de | 154 |
| &nbsp;&nbsp;it | 148 |
| &nbsp;&nbsp;nl | 172 |
| &nbsp;&nbsp;cn | 97 |
| &nbsp;&nbsp;zh-Hant | 159 |
| Unpublished articles skipped | 23 |
| Curated overview pages created | 7 |
| Images downloaded | 2055 |
| Image downloads refused (HTTP 403) | 1 |
| Dead legacy image links (support.snagr.co.uk) | 228 unique URLs, 1805 references on 167 pages |
| Embedded videos kept (Vimeo/YouTube iframes) | 63 |
| Dead internal links removed (text kept) | 69 |

## How the mapping was rebuilt

The questions export has an empty `category_id` column, so article placement was recovered by crawling the live site (`snagr.helpjuice.com`): every `/_questions/<id>` page carries `category-id` and `current-language` meta tags. Article order inside a category follows the order shown on the Helpjuice category pages where available, otherwise creation date.

## Login-only sections (not published)

These articles live in categories that require a Helpjuice login, so the crawl could not confirm their category. They were placed by title and are generated under `en/aahk-trd/`, `en/aahk-cwd/` and `en/power-bi-integration/`, which `.mintignore` excludes from the build. To publish them, remove those lines from `.mintignore` and add the groups below to the `en` entry in `docs.json`.

- TRD Admin Training Video -> AAHK-TRD
- How can I link documents to a form? (Older version) -> Forms > Link Issues and Documents to Forms
- Video Tutorial - NQAA -> AAHK-TRD > NQAA
- Website - Export PDF / PDF in batch -> AAHK-TRD > NQAA
- App - Login -> AAHK-TRD > NQAA
- Website - Form Closed (Passed) / (Failed) -> AAHK-TRD > NQAA
- Website - Fill in form and attach document -> AAHK-TRD > NQAA
- Website - Login with 2-factor authentication code -> AAHK-TRD > NQAA
- How to make use of form finder in app? -> AAHK-TRD
- Video Tutorial - DOWL -> AAHK-TRD > DOWL
- Website - Form Creation -> AAHK-TRD > NQAA
- App - Create a new inspection -> AAHK-TRD > NQAA
- App - Form Closed (Passed) / (Failed) -> AAHK-TRD > NQAA
- App - Open form from Dashboard -> AAHK-TRD > NQAA
- App - Notification -> AAHK-TRD > NQAA
- Video Tutorial - SPE Report -> AAHK-TRD > SPE Report
- Website - Photo Diary - Issue Dashboard -> AAHK-CWD > Photo Diary
- Website - Photo Dairy - Create a Photo Diary record -> AAHK-CWD > Photo Diary
- APP - Photo Dairy - Create a Photo Diary record -> AAHK-CWD > Photo Diary
- APP - Photo Dairy - Synchronisation -> AAHK-CWD > Photo Diary
- APP - Photo Diary - Adding more photos in the same record -> AAHK-CWD > Photo Diary
- How do I get my API token? -> Power BI Integration > API Doc
- Where do I find SnagR API documentation? -> Power BI Integration > API Doc
- How do I embed Power BI reports in SnagR project sites? -> Power BI Integration > Publish
- Handout Material - SPE Report -> AAHK-TRD > SPE Report
- Handout Material - NQAA -> AAHK-TRD > NQAA
- Handout Material - DOWL -> AAHK-TRD > DOWL
- How to generate photo links? -> Power BI Integration > Links
- How to generate plan viewer link to view issues? -> Power BI Integration > Links
- How to generate link to view inspection form? -> Power BI Integration > Links
- 如何添加一个缺陷？ -> 缺陷模式 > 添加缺陷

```json
[
  {
    "group": "AAHK-CWD",
    "pages": [
      {
        "group": "Photo Diary",
        "pages": [
          "en/aahk-cwd/photo-diary/website-photo-diary-issue-dashboard",
          "en/aahk-cwd/photo-diary/website-photo-dairy-create-a-photo-diary-record",
          "en/aahk-cwd/photo-diary/app-photo-dairy-create-a-photo-diary-record",
          "en/aahk-cwd/photo-diary/app-photo-dairy-synchronisation",
          "en/aahk-cwd/photo-diary/photo-diary-adding-more-photos-in-the-same-record"
        ]
      }
    ]
  },
  {
    "group": "AAHK-TRD",
    "pages": [
      "en/aahk-trd/trd-admin-training-video",
      "en/aahk-trd/how-to-make-use-of-form-finder-in-app",
      {
        "group": "DOWL",
        "pages": [
          "en/aahk-trd/dowl/app-login",
          "en/aahk-trd/dowl/handout-material-dowl-hints-and-tips"
        ]
      },
      {
        "group": "NQAA",
        "pages": [
          "en/aahk-trd/nqaa/trd-nqaa-training-video",
          "en/aahk-trd/nqaa/nqaa-training-video-website",
          "en/aahk-trd/nqaa/nqaa-training-video-app",
          "en/aahk-trd/nqaa/website-form-closed-passed-failed",
          "en/aahk-trd/nqaa/website-fill-in-form-and-attach-document",
          "en/aahk-trd/nqaa/website-login-with-2-factor-authentication-code",
          "en/aahk-trd/nqaa/website-form-creation",
          "en/aahk-trd/nqaa/app-create-a-new-inspection",
          "en/aahk-trd/nqaa/app-form-closed-passed-failed",
          "en/aahk-trd/nqaa/app-open-form-from-dashboard",
          "en/aahk-trd/nqaa/app-notification",
          "en/aahk-trd/nqaa/handout-material-nqaa"
        ]
      },
      {
        "group": "SPE Report",
        "pages": [
          "en/aahk-trd/spe-report/video-tutorials-spe-report",
          "en/aahk-trd/spe-report/training-handout-spe"
        ]
      }
    ]
  },
  {
    "group": "Power BI Integration",
    "pages": [
      {
        "group": "API Doc",
        "pages": [
          "en/power-bi-integration/api-doc/how-do-i-get-my-api-token",
          "en/power-bi-integration/api-doc/where-do-i-find-snagr-api-documentation"
        ]
      },
      {
        "group": "Links",
        "pages": [
          "en/power-bi-integration/links/how-to-generate-photo-links",
          "en/power-bi-integration/links/how-to-generate-plan-viewer-link",
          "en/power-bi-integration/links/how-to-generate-link-to-view-inspection-form"
        ]
      },
      {
        "group": "Publish",
        "pages": [
          "en/power-bi-integration/publish/how-do-i-embed-power-bi-dashboards-in-snagr-project-sites"
        ]
      }
    ]
  }
]
```

## Skipped articles

- Snagr ltd Glossary (614229): the export only contains an empty glossary widget, no terms.

Unpublished on Helpjuice (not migrated):

- Untitled Question (264202)
- Can SnagR store documents? (264216)
- How do I see list of all issues and forms? (264217)
- What does synchronise mean? (264212)
- How do I change drawing? (264213)
- What is the difference between issue mode and form mode? (264214)
- What does synchronise mean? (264219)
- How do I change drawing? (264220)
- Untitled Question (264290)
- Supporting Video (702731)
- DOWL Essentials: Your User Workflow Guide (3409410)
- How to login with Two - Factor Authentication? (356448)
- Hoe kan ons probleemherstelproces worden gedefinieerd in SnagR? (402592)
- 開發者 (384098)
- Untitled Question (292116)
- 分判商 (384045)
- 主承辦商 (384047)
- 生產商 (384111)
- 我可以按其內容搜索檢查表格嗎？ (386759)
- 如何查看和提交許可證？ (386786)
- How to create a Hierarchical List? (387513)
- How can I remove a form template from an inspection template? (387514)
- Can I remove the inspection template at company level? (387515)

## Missing images

Old articles embedded images from the retired Confluence site `support.snagr.co.uk` (offline, not in the Wayback Machine). Those image tags were removed and each affected page starts with a `{/* TODO ... */}` comment. Pages affected:

- `cn/admin/drawings/312905` (1 images)
- `cn/issues/add-issues/305044` (1 images)
- `de/aktionspunkte/aktionspunkte-aktualisieren/kann-ich-ein-aktionspunkt-erneut-eroffnen` (11 images)
- `de/aktionspunkte/aktionspunkte-finden/kan-ik-actiepunten-op-tekeningen-filteren` (21 images)
- `de/berichterstattung/statistik/wie-verschaffe-ich-mir-einen-uberblick-uber-alle-inspektionsformulare` (10 images)
- `de/dokumente/dokumente-verwalten/gibt-es-eine-versionsverwaltung-in-snagr-dokumenten` (1 images)
- `de/formulare/formulare-hinzufugen/wie-kann-ich-genehmigungen-anzeigen-und-hinzufugen` (8 images)
- `de/formulare/formulare-suchen-und-bearbeiten/kann-ich-anhand-des-inhalts-nach-inspektionsformularen-suchen` (15 images)
- `de/haufig-gestellte-fragen/bereit-fur-den-mobilen-einsatz/ubersicht-aller-icons-buttons-in-der-app` (26 images)
- `de/haufig-gestellte-fragen/lokation/lokation-abmelden` (6 images)
- `de/haufig-gestellte-fragen/lokation/lokation-schlieen-ubergeben` (30 images)
- `de/haufig-gestellte-fragen/lokation/lokation-zur-inspektion-bereit` (12 images)
- `de/projekt-einrichten/allgemeine-einstellungen/begriffe-auf-unternehmensebene` (12 images)
- `de/projekt-einrichten/allgemeine-einstellungen/prioritaten-und-enddatum-bearbeiten-auf-unternehmensebene` (8 images)
- `de/projekt-einrichten/allgemeine-einstellungen/projekte-bearbeiten-anzeigen-auf-unternehmensebene` (4 images)
- `de/projekt-einrichten/allgemeine-einstellungen/projekteinstellungen-bearbeiten-auf-projektebene` (5 images)
- `de/projekt-einrichten/allgemeine-einstellungen/regionen-bereiche-programme-auf-unternehmensebene` (18 images)
- `de/projekt-einrichten/allgemeine-einstellungen/standardsprache-oder-logo-bearbeiten-auf-unternehmensebene` (4 images)
- `de/projekt-einrichten/checklisten-und-zeitplane-business-level/construction-stages-erstellen` (16 images)
- `de/projekt-einrichten/checklisten-und-zeitplane-business-level/projekt-checklisten-importieren-auf-projektebene` (11 images)
- `de/projekt-einrichten/checklisten-und-zeitplane-business-level/projektcheckliste-erstellen` (6 images)
- `de/projekt-einrichten/formulare-unternehmensebene/kann-ich-das-formularbild-bearbeiten-ersetzen` (11 images)
- `de/projekt-einrichten/formulare-unternehmensebene/kann-ich-eine-inspektionsvorlage-auf-unternehmensebene-loschen` (8 images)
- `de/projekt-einrichten/formulare-unternehmensebene/wie-entferne-ich-eine-formularvorlage-aus-einer-inspektionsvorlage` (9 images)
- `de/projekt-einrichten/formulare-unternehmensebene/wie-erstellen-sie-eine-hierarchische-liste` (8 images)
- `de/projekt-einrichten/formulare-unternehmensebene/wie-kann-ich-eine-inspektionsvorlage-bearbeiten` (10 images)
- `de/projekt-einrichten/genehmigungen-geschaftsniveau/genehmigungsformularseite-hinzufugen` (9 images)
- `de/projekt-einrichten/genehmigungen-geschaftsniveau/genehmigungsprufungen-anzeigen-bearbeiten-loschen` (19 images)
- `de/projekt-einrichten/genehmigungen-geschaftsniveau/genehmigungsprufungen-hinzufugen` (6 images)
- `de/projekt-einrichten/konten-und-rechte-firmensebene/benutzerverwaltung-auf-unternehmensebene` (17 images)
- `de/projekt-einrichten/konten-und-rechte-firmensebene/vertragsmanagement-auf-unternehmensebene` (16 images)
- `de/projekt-einrichten/lokation-projektebene/wie-erstelle-ich-barcodes-qr-codes-fur-lokationen` (6 images)
- `de/projekt-einrichten/lokation-projektebene/wie-verschiebe-bearbeite-losche-ich-eine-lokationensnadel` (22 images)
- `de/projekt-einrichten/zeichnungen-projektebene/was-sind-zeichnungfelde-und-wie-setze-ich-sie` (5 images)
- `en/documents/upload-document/is-there-version-control-in-snagr-documents` (1 images)
- `en/faq/get-ready-on-mobile/icons-or-buttons-on-the-device` (28 images)
- `en/faq/locations/location-ready-for-inspection` (17 images)
- `en/faq/locations/location-sign-off` (30 images)
- `en/faq/locations/room-area-signoff` (6 images)
- `en/forms/find-and-edit-forms/can-i-search-inspection-forms-by-the-hotspot-value` (15 images)
- `en/forms/find-and-edit-forms/how-do-i-see-form-notifications` (7 images)
- `en/forms/find-and-edit-forms/inspection-dashboard` (10 images)
- `en/forms/submit-forms/permits-dashboard` (8 images)
- `en/issues/add-issues/can-i-copy-and-paste-an-issue` (2 images)
- `en/issues/find-issues/filtering-issues-on-device` (22 images)
- `en/set-up-project/accounts-and-permissions-company-level/add-contractors-at-the-company-level` (16 images)
- `en/set-up-project/accounts-and-permissions-company-level/add-user-at-the-company-level` (17 images)
- `en/set-up-project/checklists-and-scheduling-company-level/construction-stages` (16 images)
- `en/set-up-project/checklists-and-scheduling-company-level/construction-stages-2` (21 images)
- `en/set-up-project/checklists-and-scheduling-company-level/project-checklists` (6 images)
- `en/set-up-project/checklists-and-scheduling-company-level/project-checklists-2` (11 images)
- `en/set-up-project/drawings-project-level/how-to-set-up-the-drawing-regions` (5 images)
- `en/set-up-project/forms-company-level/can-i-edit-replace-inspection-form` (11 images)
- `en/set-up-project/forms-company-level/how-can-i-remove-a-form-from-the-inspection-template` (9 images)
- `en/set-up-project/forms-company-level/how-can-i-remove-the-inspection-from-the-company` (8 images)
- `en/set-up-project/forms-company-level/how-to-create-a-hierarchical-list` (9 images)
- `en/set-up-project/forms-company-level/how-to-edit-form-details` (7 images)
- `en/set-up-project/forms-company-level/how-to-edit-the-inspection-template` (9 images)
- `en/set-up-project/general-settings/can-i-edit-the-priorities-and-due-day` (8 images)
- `en/set-up-project/general-settings/edit-default-language-or-logo` (4 images)
- `en/set-up-project/general-settings/edit-view-projects` (4 images)
- `en/set-up-project/general-settings/how-to-edit-the-project-settings` (5 images)
- `en/set-up-project/general-settings/regions-divisions-programs` (18 images)
- `en/set-up-project/general-settings/terminology` (12 images)
- `en/set-up-project/locations-project-level/create-barcode-for-location` (1 images)
- `en/set-up-project/locations-project-level/how-to-set-up-locations-on-drawings` (16 images)
- `en/set-up-project/locations-project-level/move-edit-delete-a-location-pin` (22 images)
- `en/set-up-project/permits-company-level/add-permit` (9 images)
- `en/set-up-project/permits-company-level/add-permit-inspection` (6 images)
- `en/set-up-project/permits-company-level/view-edit-delete-permit-inspection` (21 images)
- `it/difetti/aggiorna-informazioni-difetto/how-to-reopen-the-issue` (11 images)
- `it/difetti/aggiungi-difetti/can-i-copy-and-paste-an-issue` (2 images)
- `it/difetti/trova-difetti/filtering-issues-on-device` (22 images)
- `it/faq/get-ready-on-mobile/icons-or-buttons-on-the-device` (29 images)
- `it/faq/siti/location-ready-for-inspection` (17 images)
- `it/faq/siti/location-sign-off` (30 images)
- `it/faq/siti/room-area-signoff` (6 images)
- `it/impostazione-progetti/checklists-e-schedulazione-amministrazione-societa/construction-stages` (16 images)
- `it/impostazione-progetti/checklists-e-schedulazione-amministrazione-societa/construction-stages-2` (21 images)
- `it/impostazione-progetti/checklists-e-schedulazione-amministrazione-societa/project-checklists` (6 images)
- `it/impostazione-progetti/checklists-e-schedulazione-amministrazione-societa/project-checklists-2` (11 images)
- `it/impostazione-progetti/disegni-amministrazione-progetto/how-to-set-up-the-drawing-regions` (5 images)
- `it/impostazione-progetti/impostazioni-generali/can-i-edit-the-priorities-and-due-day` (8 images)
- `it/impostazione-progetti/impostazioni-generali/edit-default-language-or-logo` (4 images)
- `it/impostazione-progetti/impostazioni-generali/edit-view-projects` (4 images)
- `it/impostazione-progetti/impostazioni-generali/how-to-edit-the-project-settings` (5 images)
- `it/impostazione-progetti/impostazioni-generali/terminology` (12 images)
- `it/impostazione-progetti/modelli-di-documento-amministrazione-societa/can-i-edit-replace-inspection-form` (11 images)
- `it/impostazione-progetti/modelli-di-documento-amministrazione-societa/how-can-i-remove-a-form-from-the-inspection-template` (9 images)
- `it/impostazione-progetti/modelli-di-documento-amministrazione-societa/how-can-i-remove-the-inspection-from-the-company` (8 images)
- `it/impostazione-progetti/modelli-di-documento-amministrazione-societa/how-to-create-a-hierarchical-list` (8 images)
- `it/impostazione-progetti/modelli-di-documento-amministrazione-societa/how-to-edit-the-inspection-template` (10 images)
- `it/impostazione-progetti/permessi-amministrazione-societa/add-permit` (9 images)
- `it/impostazione-progetti/permessi-amministrazione-societa/add-permit-inspection` (6 images)
- `it/impostazione-progetti/permessi-amministrazione-societa/view-edit-delete-permit-inspection` (21 images)
- `it/impostazione-progetti/siti-amministrazione-progetto/create-barcode-for-location` (6 images)
- `it/impostazione-progetti/siti-amministrazione-progetto/how-to-set-up-locations-on-drawings` (16 images)
- `it/impostazione-progetti/siti-amministrazione-progetto/move-edit-delete-a-location-pin` (22 images)
- `it/impostazione-progetti/utenti-e-permessi-amministrazione-societa/add-contractors-at-the-company-level` (16 images)
- `it/impostazione-progetti/utenti-e-permessi-amministrazione-societa/add-user-at-the-company-level` (17 images)
- `it/ispezioni/finalizza-documenti-di-ispezione/permits-dashboard` (8 images)
- `it/ispezioni/trova-ed-aggiorna-documenti-di-ispezione/can-i-search-inspection-forms-by-the-hotspot-value` (15 images)
- `it/ispezioni/trova-ed-aggiorna-documenti-di-ispezione/how-do-i-see-form-notifications` (8 images)
- `it/ispezioni/trova-ed-aggiorna-documenti-di-ispezione/inspection-dashboard` (10 images)
- `it/repositorio-documenti/gestisci-documenti/is-there-version-control-in-snagr-documents` (1 images)
- `nl/actiepunten/actiepunten-updaten/kan-ik-een-actiepunt-heropenen` (11 images)
- `nl/actiepunten/actiepunten-vinden/kan-ik-actiepunten-op-tekeningen-filteren` (22 images)
- `nl/documenten/documenten-beheren/is-er-versiebeheer-in-snagr-documenten` (1 images)
- `nl/formulieren/formulieren-toevoegen/hoe-bekijk-en-voeg-ik-vergunningen-toe` (8 images)
- `nl/formulieren/formulieren-vinden-en-bewerken/kan-ik-naar-inspectieformulieren-zoeken-aan-de-hand-van-de-inhoud` (15 images)
- `nl/project-opzetten/accounts-en-rechten-bedrijfsniveau/aannemersbeheer-op-bedrijfsniveau` (16 images)
- `nl/project-opzetten/accounts-en-rechten-bedrijfsniveau/gebruikersbeheer-op-bedrijfsniveau` (17 images)
- `nl/project-opzetten/algemene-instellingen/bewerk-bekijk-projecten-op-bedrijfsniveau` (4 images)
- `nl/project-opzetten/algemene-instellingen/prioriteiten-en-einddatum-bewerken-op-bedrijfsniveau` (8 images)
- `nl/project-opzetten/algemene-instellingen/project-instellingen-bewerken-op-project-niveau` (5 images)
- `nl/project-opzetten/algemene-instellingen/regio-s-divisies-programma-s-op-bedrijfsniveau` (18 images)
- `nl/project-opzetten/algemene-instellingen/standaard-taal-of-logo-bewerken-op-bedrijfsniveau` (4 images)
- `nl/project-opzetten/algemene-instellingen/termen-op-bedrijfsniveau` (12 images)
- `nl/project-opzetten/checklijsten-en-schema-s-bedrijfsniveau/importeer-project-checklijsten-op-projectniveau` (11 images)
- `nl/project-opzetten/checklijsten-en-schema-s-bedrijfsniveau/maak-construction-stages` (16 images)
- `nl/project-opzetten/checklijsten-en-schema-s-bedrijfsniveau/project-checklijst-maken` (6 images)
- `nl/project-opzetten/formulieren-bedrijfsniveau/hoe-bewerk-je-formulier-details` (7 images)
- `nl/project-opzetten/formulieren-bedrijfsniveau/hoe-kan-ik-een-inspectie-sjabloon-bewerken` (10 images)
- `nl/project-opzetten/formulieren-bedrijfsniveau/hoe-maak-je-een-hierarchische-lijst` (9 images)
- `nl/project-opzetten/formulieren-bedrijfsniveau/hoe-ontwerp-ik-een-inspectie-formulier-template-met-bedrijfslogica-erin` (3 images)
- `nl/project-opzetten/formulieren-bedrijfsniveau/hoe-verwijder-ik-een-formulier-template-uit-een-inspectie-template` (9 images)
- `nl/project-opzetten/formulieren-bedrijfsniveau/kan-ik-de-formulierafbeelding-bewerken-vervangen` (11 images)
- `nl/project-opzetten/formulieren-bedrijfsniveau/kan-ik-een-inspectie-template-verwijderen-op-bedrijfsniveau` (8 images)
- `nl/project-opzetten/locaties-projectniveau/hoe-genereer-ik-barcodes-qr-codes-voor-locaties` (6 images)
- `nl/project-opzetten/locaties-projectniveau/hoe-verplaats-bewerk-verwijder-ik-een-locatie-pin` (22 images)
- `nl/project-opzetten/tekeningen-projectniveau/wat-zijn-tekening-vakken-en-hoe-stel-ik-ze-in` (5 images)
- `nl/project-opzetten/vergunningen-bedrijfsniveau/bekijk-bewerk-verwijder-vergunning-inspecties` (20 images)
- `nl/project-opzetten/vergunningen-bedrijfsniveau/vergunning-inspectie-toevoegen` (6 images)
- `nl/project-opzetten/vergunningen-bedrijfsniveau/vergunningsformulier-pagina-toevoegen` (9 images)
- `nl/veelgestelde-vragen/klaar-voor-mobiel-gebruik/overzicht-van-alle-iconen-knoppen-in-de-app` (28 images)
- `nl/veelgestelde-vragen/locaties/locatie-aftekenen` (30 images)
- `nl/veelgestelde-vragen/locaties/locatie-aftekenen-2` (6 images)
- `nl/veelgestelde-vragen/locaties/locatie-gereed-voor-inspectie` (14 images)
- `nl/verslaglegging/statistieken/hoe-krijg-ik-een-overzicht-van-alle-inspectieformulieren` (10 images)
- `zh-hant/faq/get-ready-on-mobile/386010` (11 images)
- `zh-hant/faq/locations/386033` (14 images)
- `zh-hant/faq/locations/386034` (21 images)
- `zh-hant/faq/locations/room-area-signoff` (4 images)
- `zh-hant/forms/find-and-edit-forms/289908` (5 images)
- `zh-hant/issues/add-issues/280576` (1 images)
- `zh-hant/issues/find-issues/386031` (22 images)
- `zh-hant/reporting/analytics/how-do-i-get-an-overview-of-all-inspection-forms` (8 images)
- `zh-hant/set-up-project/accounts-and-permissions-company-level/403231` (6 images)
- `zh-hant/set-up-project/accounts-and-permissions-company-level/manage-user-at-company-level` (6 images)
- `zh-hant/set-up-project/checklists-and-scheduling-company-level/create-construction-stages` (8 images)
- `zh-hant/set-up-project/checklists-and-scheduling-company-level/create-project-checklist` (4 images)
- `zh-hant/set-up-project/checklists-and-scheduling-company-level/import-construction-stages-schedules-to-track-progress-at-project-level` (17 images)
- `zh-hant/set-up-project/drawings-project-level/312833` (1 images)
- `zh-hant/set-up-project/forms-company-level/440931` (6 images)
- `zh-hant/set-up-project/forms-company-level/can-i-edit-replace-form-page-image` (8 images)
- `zh-hant/set-up-project/forms-company-level/how-can-i-edit-an-inspection-template` (6 images)
- `zh-hant/set-up-project/general-settings/edit-default-language-or-logo-at-company-level` (3 images)
- `zh-hant/set-up-project/general-settings/edit-priorities-and-due-days-at-company-level` (4 images)
- `zh-hant/set-up-project/general-settings/edit-project-settings-at-project-level` (2 images)
- `zh-hant/set-up-project/general-settings/edit-view-projects-at-company-level` (4 images)
- `zh-hant/set-up-project/general-settings/regions-divisions-programs-at-company-level` (13 images)
- `zh-hant/set-up-project/general-settings/terminology-at-company-level` (3 images)
- `zh-hant/set-up-project/locations-project-level/how-to-generate-qr-codes-for-locations` (5 images)
- `zh-hant/set-up-project/locations-project-level/how-to-move-edit-delete-a-location-pin` (12 images)
- `zh-hant/set-up-project/permits-company-level/add-permit-form-pages` (6 images)
- `zh-hant/set-up-project/permits-company-level/add-permit-inspection` (3 images)
- `zh-hant/set-up-project/permits-company-level/view-edit-delete-permit-inspection` (16 images)

Refused downloads:

- https://static.helpjuice.com/helpjuice_production/uploads/upload/image/3577/direct/1539333726044-Admin_Website.001.jpeg (fail: HTTP Error 403: Forbidden) used on question(s) 343363, 356462, 359634

## Dead internal links

These hrefs pointed to deleted or unpublished Helpjuice articles (they 404 on the live site too). The link was dropped and the link text kept.

- `/_questions/321271` (6x)
- `/_questions/264255` (5x)
- `/_questions/266212` (5x)
- `https://snagr.helpjuice.com/nl-koppel-actiepunten-en-documenten-aan-formulieren/nl-how-can-i-link-issues-to-a-form?from_search=21044981` (4x)
- `https://snagr.helpjuice.com/nl-workflow-en-gebruikersrechten/nl-how-can-our-issue-rectification-process-be-defined-in-snagr?kb_language=nl_NL` (4x)
- `https://snagr.helpjuice.com/nl-documenten-beheren/nl-what-is-bundle?kb_language=nl_NL` (4x)
- `https://snagr.helpjuice.com/nl-rapporten-en-statistieken/nl-can-issue-reports-be-generated-automatically?kb_language=nl_NL` (4x)
- `/_categories/36877` (3x)
- `https://snagr.helpjuice.com/drawings/how-should-drawing-sets-be-set-up` (2x)
- `https://snagr.helpjuice.com/nl-actiepunten-toevoegen/nl-how-to-add-an-issue?from_search=21044847` (2x)
- `https://snagr.helpjuice.com/nl-rapporten-en-statistieken/nl-how-to-generate-an-issue-report?from_search=21044866` (2x)
- `https://snagr.helpjuice.com/nl-notificaties/nl-how-to-set-up-issues-notifications-for-all-users?from_search=21044875` (2x)
- `https://snagr.helpjuice.com/nl-actiepunten?kb_language=nl_NL` (2x)
- `https://snagr.helpjuice.com/nl-setup-in-app/nl-why-should-i-synchronise?from_search=21044898vv` (2x)
- `https://snagr.helpjuice.com/nl-introductie/nl-overview-for-inspection-teams-consultants?from_search=21044902` (2x)
- `https://snagr.helpjuice.com/nl-rapporten-en-statistieken/nl-how-do-i-view-analytics?from_search=21044786` (2x)
- `https://snagr.helpjuice.com/admin/t_CN/categories/new` (2x)
- `Please%20download%20the%20NQAA%20one%20pager%20here.` (1x)
- `/_questions/402592` (1x)
- `Erfahren%20Sie,%20wie%20Sie%20mehrere%20Aktionspunkte%20gleichzeitig%20bearbeiten.` (1x)
- `/_questions/266536` (1x)
- `/issues` (1x)
- `https://snagr.helpjuice.com/nl-exporteer-formulieren-naar-pdf/nl-can-i-extract-a-list-of-forms-that-are-created-on-snagr?kb_language=nl_NL` (1x)
- `https://snagr.helpjuice.com/nl-tekeningen/nl-how-to-prepare-and-upload-drawings?kb_language=nl_NL` (1x)
- `https://snagr.helpjuice.com/nl-tekeningen/nl-how-to-set-up-locations-on-drawings?kb_language=nl_NL` (1x)
- `https://snagr.helpjuice.com/nl-tekeningen?kb_language=nl_NL` (1x)
- `https://snagr.helpjuice.com/nl-documenten?kb_language=nl_NL` (1x)
- `/algemeen/2ta` (1x)
- `https://snagr.helpjuice.com/nl-gebruikersaccounts/nl-how-to-add-users-to-project?kb_language=nl_NL` (1x)
- `https://snagr.helpjuice.com/algemeen/2sa` (1x)
- `https://snagr.helpjuice.com/nl-tekeningen/nl-how-to-group-drawings?kb_language=nl_NL` (1x)
- `/_questions/264205` (1x)
- `/44032/318872` (1x)

## Curated overview pages

Helpjuice starter-guide categories had no articles of their own but listed links to articles elsewhere. Those became `index.mdx` pages with the same link list.

- `en/getting-started/starter-guide-how-do-i-take-issues/index` - Starter Guide: How do I take issues? (9 links)
- `en/getting-started/starter-guide-how-to-submit-forms/index` - Starter Guide: How to submit forms? (9 links)
- `en/reporting/standard-pdf-report/index` - Standard PDF Report (5 links)
- `en/new-features/document-repository-upgrade/index` - Document repository (Upgrade) (2 links)
- `en/new-features/others/index` - Others (4 links)
- `it/reportistica/reportistica-standard-pdf/index` - Reportistica Standard PDF (4 links)
- `zh-hant/getting-started/starter-guide-how-to-submit-forms/index` - 初階指引：如何提交表格？ (1 links)

## Duplicate slugs

Two articles in the same folder had the same Helpjuice codename; the second one got a `-2` suffix.

- 如何將附有缺陷或者文檔的表格導出為PDF文件？ -> `zh-hant/forms/export-forms/pdf-2`
- Import Project Checklists (at Project level) -> `en/set-up-project/checklists-and-scheduling-company-level/project-checklists-2`
- Importa Checklist di Progetto (Amministrazione progetto) -> `it/impostazione-progetti/checklists-e-schedulazione-amministrazione-societa/project-checklists-2`
- Import Construction Stages Schedules to track progress (at Project Level) -> `en/set-up-project/checklists-and-scheduling-company-level/construction-stages-2`
- Fasi di Costruzione: importazione a livello Progetto -> `it/impostazione-progetti/checklists-e-schedulazione-amministrazione-societa/construction-stages-2`
- 如何将附有缺陷或者文档的表格导出为PDF文件？ -> `cn/forms/export-forms/pdf-2`
- Locatie Aftekenen -> `nl/veelgestelde-vragen/locaties/locatie-aftekenen-2`
- SnagR支援哪些系統版本？ -> `zh-hant/faq/general/snagr-2`

## Things to review by hand

- Branding: `docs.json` still uses the starter logo files in `logo/` and `favicon.svg`; replace them with SnagR assets. The navbar links, footer socials and starter pages were removed.
- Colours: primary `#086F92` was derived from the old Helpjuice theme (`#09b2e6` failed the WCAG contrast check).
- Chinese article URLs: Helpjuice used numeric codenames for most Chinese articles, so their file names are the Helpjuice question ids (for example `zh-hant/issues/add-issues/280009.mdx`). Rename them if you want readable URLs; nothing links to the old codenames.
- Group names in the sidebar keep the original Helpjuice category names, including capitalisation and the typo in "Troubelshooting for Admins".
- Guidde walkthroughs were flattened to their screenshots and step text.
- Some tiny icon images (device/website markers) use their file name as alt text.

