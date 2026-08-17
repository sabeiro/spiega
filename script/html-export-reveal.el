;;; -*- mode: lisp; coding: utf-8; -*-
;;; HTML Export Configuration for Org Files - Body Content Only
;;; Version: 3.0
;;; Author: sabeiro

;;; Commentary:
;; This file configures org-mode HTML export to output only body content
;; Usage: emacs file.org --batch --load emacs/org-html-export-html-conf.el -f org-html-export-to-html --kill

;;; Code:
(add-to-list 'load-path (expand-file-name "~/.emacs.d/lisp/"))
(setq package-enable-at-startup nil)
;; Bootstrap straight.el
(defvar bootstrap-version)
(let ((bootstrap-file
       (expand-file-name "straight/repos/straight.el/bootstrap.el"
                         user-emacs-directory))
      (bootstrap-version 7))
  (unless (file-exists-p bootstrap-file)
    (with-current-buffer
        (url-retrieve-synchronously
         "https://raw.githubusercontent.com/radian-software/straight.el/develop/install.el"
         'silent 'inhibit-cookies)
      (goto-char (point-max))
      (eval-print-last-sexp)))
  (load bootstrap-file nil 'nomessage))
(straight-use-package 'use-package)
(setq straight-use-package-by-default t)
(straight-use-package 'org)

(use-package package)
(setq package-archives
      '(("melpa" . "https://melpa.org/packages/")
	("melpa-stable" . "https://stable.melpa.org/packages/")
	("gnu" . "https://elpa.gnu.org/packages/")
	("nongnu" . "https://elpa.nongnu.org/nongnu/")))
(setq package-archive-priorities
      '(("melpa-stable" . 10)
	("gnu" . 7)
	("melpa" . 5)))

(require 'ox-publish)
;; (use-package ox-hugo)
(use-package ox-reveal)
(setq org-reveal-root "../reveal/")
(setq org-re-reveal-root "../reveal/")
;;(setq org-reveal-external-plugins '((RevealMenu . "{ src: '../reveal/js/head.js', async: true, condition: function() { return !!document.body.classList; } },")))

(setq org-reveal-hlevel 1) ;; from second level vertical
(use-package oer-reveal)
(setq oer-reveal-publish-org-publishing-functions
      '(oer-reveal-publish-to-reveal))


;;; Disable org's built-in style features to output clean body-only content
(defun my-org-disable-builtin-style ()
  "Disable org's builtin style features."
  (interactive)
  (setq org-html-htmlize-styles nil)
  org-html-inline-source
  (setq org-html-inline-source nil)
  org-html-id-shortcuts
  (setq org-html-id-shortcuts nil)
  org-html-link-attributes
  (setq org-html-link-attributes nil)
  org-html-macros
  (setq org-html-macros nil))

;;(require 'htmlize)
;; Body-only export options (no HTML wrapper, no TOC, no footers)
(setq org-html-toc nil
      org-html-footnotes-in-header-file nil
      org-html-footnotes-after-body nil
      org-html-footnotes-as-uid t
      org-export-with-broken-links t
      org-export-with-toc nil
      org-export-with-section-numbers nil
      org-export-with-sub-superscripts nil
      org-html-verbatim "verbatim"
      org-use-sub-superscripts nil
      org-html-wrap-src-lines t
      org-html-prefer-user-labels t
      org-export-babel-evaluate nil 
      org-html-footer nil
      )
