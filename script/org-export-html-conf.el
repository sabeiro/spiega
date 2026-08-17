;;; -*- mode: lisp; coding: utf-8; -*-
;;; HTML Export Configuration for Org Files - Complete Emacs Org Export Setup
;;; Version: 2.1 (Fixed htmlize output)
;;; Author: sabeiro
;;; Created: 2026-06-05

;; =============================================================================
;; CUSTOM STYLES
;; =============================================================================

(defun org-export-html-insert-my-custom-style ()
  "Insert custom styles for HTML export."
  (let ((styles
         (concat
          "/* ============================================ "
          "CUSTOM ORG SLIDES STYLES "
          "============================================ */\n"
          ":root {\n"
          "  --primary-color: #ff3002;\n"
          "  --secondary-color: #212121;\n"
          "  --accent-color: #00aaff;\n"
          "  --bg-primary: #ffffff;\n"
          "  --bg-secondary: #f8f9fa;\n"
          "  --code-bg: #1e1e1e;\n"
          "  --code-text: #d4d4d4;\n"
          "  --border-color: #e0e0e0;\n"
          "  --border-radius: 8px;\n"
          "  --font-stack: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif;\n"
          "  --monospace-stack: \"SF Mono\", Monaco, \"Cascadia Code\", \"Inconsolata\", \"Fira Mono\", monospace;\n"
          "}\n"
          "\n"
          "/* Animations */\n"
          "@keyframes fadeUp {\n"
          "  from { opacity: 0; transform: translateY(40px); }\n"
          "  to { opacity: 1; transform: translateY(0); }\n"
          "}\n"
          "@keyframes slideIn {\n"
          "  from { opacity: 0; transform: translateX(30px); }\n"
          "  to { opacity: 1; transform: translateX(0); }\n"
          "}\n"
          "\n"
          "/* Main Container */\n"
          ".slides-container {\n"
          "  padding: 2rem;\n"
          "  font-family: var(--font-stack);\n"
          "  line-height: 1.6;\n"
          "  background: var(--bg-primary);\n"
          "  max-width: 1200px;\n"
          "  margin: 0 auto;\n"
          "  color: var(--secondary-color);\n"
          "}\n"
          "\n"
          "/* Slide Container */\n"
          ".slide {\n"
          "  background: var(--bg-primary);\n"
          "  margin-bottom: 3rem;\n"
          "  padding: 2.5rem;\n"
          "  border-radius: var(--border-radius);\n"
          "  box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 1px 3px rgba(0,0,0,0.08);\n"
          "  border: 1px solid var(--border-color);\n"
          "  min-height: 500px;\n"
          "  position: relative;\n"
          "}\n"
          "\n"
          "/* Slide Header */\n"
          ".slide h2 {\n"
          "  margin-top: 0;\n"
          "  margin-bottom: 1.5rem;\n"
          "  padding-bottom: 0.5rem;\n"
          "  border-bottom: 4px solid var(--primary-color);\n"
          "  color: var(--primary-color);\n"
          "  font-size: 2rem;\n"
          "  font-weight: 600;\n"
          "}\n"
          "\n"
          "/* Slide Content */\n"
          ".slide-content {\n"
          "  white-space: pre-wrap;\n"
          "  word-wrap: break-word;\n"
          "}\n"
          "\n"
          "/* Links */\n"
          ".org-link, .link-btn {\n"
          "  color: var(--primary-color);\n"
          "  text-decoration: underline;\n"
          "  font-weight: 500;\n"
          "}\n"
          "\n"
          "/* Code Blocks */\n"
          "pre {\n"
          "  background: var(--code-bg);\n"
          "  color: var(--code-text);\n"
          "  padding: 1.5rem;\n"
          "  border-radius: var(--border-radius);\n"
          "  overflow-x: auto;\n"
          "}\n"
          "\n"
          "/* Inline Code */\n"
          "code:not(.source-block) {\n"
          "  background: #f1f5f9;\n"
          "  color: #d63384;\n"
          "  padding: 0.3rem 0.6rem;\n"
          "  border-radius: 4px;\n"
          "  font-family: var(--monospace-stack);\n"
          "  font-size: 0.9em;\n"
          "}\n"
          "\n"
          "/* Blockquote */\n"
          "blockquote {\n"
          "  margin: 1.5rem 0;\n"
          "  padding-left: 1rem;\n"
          "  border-left: 4px solid var(--primary-color);\n"
          "  color: #666;\n"
          "}\n"
          "\n"
          "/* Callout Boxes */\n"
          ".note-box {\n"
          "  background: var(--secondary-color);\n"
          "  padding: 1rem;\n"
          "  border-radius: 6px;\n"
          "  margin: 1rem 0;\n"
          "  color: #fff;\n"
          "}\n"
          "\n"
          "/* Lists */\n"
          "ul, ol {\n"
          "  margin: 0.5rem 0;\n"
          "  padding-left: 1.5rem;\n"
          "}\n"
          "li {\n"
          "  margin: 0.25rem 0;\n"
          "}\n"
          "\n"
          "/* Tables */\n"
          "table {\n"
          "  width: 100%;\n"
          "  border-collapse: collapse;\n"
          "  margin: 1rem 0;\n"
          "}\n"
          "th, td {\n"
          "  border-bottom: 1px solid var(--border-color);\n"
          "  padding: 0.5rem 0.8rem;\n"
          "  text-align: left;\n"
          "}\n"
          "th {\n"
          "  background-color: var(--primary-color);\n"
          "  color: white;\n"
          "  font-weight: 600;\n"
          "}\n"
          "\n"
          "/* Subslides */\n"
          ".subslide {\n"
          "  border-left: 4px solid var(--accent-color);\n"
          "  padding-left: 1.5rem;\n"
          "  margin-left: -1.5rem;\n"
          "}\n"
          "\n"
          "/* Images */\n"
          "img {\n"
          "  max-width: 100%;\n"
          "  height: auto;\n"
          "  border-radius: var(--border-radius);\n"
          "}\n"
          "))"
          (insert styles)
          (newline))))

;; Load custom styles
(add-hook 'org-html-before-export-hook #'org-export-html-insert-my-custom-style)
(setq package-install-upgrade-built-in t)
(progn (unload-feature 'transient t) (require 'transient))
(straight-use-package 'org)
;; =============================================================================
;; DEFAULT EXPORT OPTIONS
;; =============================================================================

(setq org-html-htmlize-output-type 'css
      org-html-mathjax-url "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
      org-html-stylesheet-file (concat default-directory "css/style.css")
      org-babel-show-only-final-results t
      org-babel-ob-default 'lisp)

(org-babel-do-load-libraries
 `((:exec ,(concat (expand-file-name "org-export-html-conf.el" (expand-file-name (file-name-directory default-directory)))))
   (:load "htmlize")
   (:load "margin")
   (:load "pretty")
   (:load "ob-clojure" "ob-emacs-lisp")
   (:html-prepender "")
   (:html-postpender "")))

;; =============================================================================
;; END OF FILE
;; =============================================================================
