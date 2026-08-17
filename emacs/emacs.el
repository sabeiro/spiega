;; ---------------------------------STYLE-------------------------------
(custom-set-variables
 '(ansi-color-faces-vector
   [default default default italic underline success warning error])
 '(ansi-color-names-vector
   ["#000044" "#d55e00" "#009e73" "#f8ec59" "#0072b2" "#cc79a7" "#56b4e9" "white"])
 '(custom-enabled-themes '(misterioso))
 '(custom-safe-themes
   '("43b0db785fc313b52a42f8e5e88d12e6bd6ff9cee5ffb3591acf51bbd465b3f4" "47aaf1021bdd742a2f91448f089ad6fe95028c9557638d4333452ce85da980de" default))
 '(fringe-mode 0 nil (fringe))
 '(global-ede-mode nil)
 '(inhibit-startup-screen t)
 '(initial-buffer-choice nil)
 '(initial-major-mode 'lisp-interaction-mode)
 ;;'(package-selected-packages '(eradio ess-R-data-view ess slack python-pytest python-black markdown-mode+ json-mode eimp auto-complete))
 '(scroll-bar-mode t)
 '(semantic-mode t)              ; was t: semantic (CEDET) often blocks file loading / startup
 '(show-paren-mode t)
 '(size-indication-mode nil)
 '(menu-bar-mode nil)
 '(tooltip-mode t)
 '(tool-bar-mode nil))
;; Basic UI tweaks
(setq inhibit-startup-message t
      ring-bell-function 'ignore
      use-dialog-box nil)
(setq org-hide-emphasis-markers t) ;; hides the emphasis markers
(setq olivetti-body-with 100)
;; this controls the color of bold, italic, underline, verbatim, strikethrough
(setq org-emphasis-alist
  '(("*" (bold :slant italic :weight black )) ;; this make bold both italic and bold, but not color change
    ("/" (italic :foreground "dark salmon" )) ;; italic text, the text will be "dark salmon"
    ("_" underline :foreground "cyan" ) ;; underlined text, color is "cyan"
    ("=" (:foreground "deep slate blue" )) ;; :background "snow1" 
    ("~" (:foreground "dim gray" )) ;; :background "PaleGreen1" 
    ("+" (:strike-through nil :foreground "dark orange" ))))
(custom-set-faces)
(add-to-list 'default-frame-alist '(foreground-color . "#E0DFDB"))
(add-to-list 'default-frame-alist '(background-color . "#110428"))
(set-frame-parameter (selected-frame) 'alpha 90)
(add-to-list 'default-frame-alist (cons 'alpha 90))
(defun toggle-transparency ()
  (interactive)
  (set-frame-parameter (selected-frame) 'alpha 95)
  (add-to-list 'default-frame-alist (cons 'alpha 95)))
(defun light-colors ()
  "High contrast for sunny days."
  (interactive)
  (set-background-color "white")
  (set-foreground-color "black"))
(defun font-big ()
  "Increase font size by 10."
  (interactive)
  (set-face-attribute 'default nil :height
                      (+ (face-attribute 'default :height) 10)))
(defun font-small ()
  "Decrease font size by 10."
  (interactive)
  (set-face-attribute 'default nil :height
                      (- (face-attribute 'default :height) 10)))
;;---------------------------binding-hooks-------------------------
(global-set-key [C-mouse-4] 'text-scale-increase)
(global-set-key [C-mouse-5] 'text-scale-decrease)
(global-set-key (kbd "M-l") 'goto-line)
(global-set-key (kbd "C-;") 'other-window)
(global-set-key (kbd "C-c l") 'light-colors)
(global-set-key (kbd "C-+") 'font-big)
(global-set-key (kbd "C--") 'font-small)
(global-set-key (kbd "C-c l") #'org-store-link)
(global-set-key (kbd "C-c a") #'org-agenda)
(global-set-key (kbd "C-c c") #'org-capture)
(add-hook
 'rst-mode-hook
 (lambda ()
   (setq-local fill-column 120)
   (setq-local indent-tabs-mode nil)
   (setq-local tab-width 3)
   (setq-local evil-shift-width 3)
   (add-to-list 'write-file-functions 'delete-trailing-whitespace)
   ;; package: find-file-in-project
   (setq-local ffip-patterns '("*.rst" "*.py"))))
;; (add-to-list 'org-structure-template-alist 
;;              '(("s"  "#+name: ?\n#+begin_src bash :export code :outputut results replace \n\n#+end_src"))
;;              '("p"  "#+name: ?\n#+begin_src python :export code :output results replace \n\n#+end_src")))
(defun my-revert-buffer-no-ask ()
  "Reload current buffer from disk without asking."
  (interactive)
  (revert-buffer t t))
(defun revert-buffer-no-confirm ()
  "Revert buffer without confirmation."
  (interactive)
  (revert-buffer :ignore-auto :noconfirm))
(global-set-key (kbd "C-c r") 'my-revert-buffer-no-ask)
;;-------------------------environment-------------------------
(prefer-coding-system 'utf-8)
(set-default-coding-systems 'utf-8)
(set-terminal-coding-system 'utf-8)
(set-keyboard-coding-system 'utf-8)	;
(set-language-environment 'utf-8)
(setenv "PATH" (concat "$LAV_DIR/bin" ":" (getenv "PATH")))
(make-directory (expand-file-name "~/lav/tmp") t)
(setq temporary-file-directory "~/lav/tmp/")
(setq small-temporary-file-directory "~/lav/tmp/")
(add-to-list 'exec-path '("~/.local/share/pnpm/bin/"))
;;----------------------------------PACKAGES---------------------------------------
;; If you're using straight.el, keep package.el from auto-loading.
(add-to-list 'load-path (expand-file-name "~/.emacs.d/lisp/"))
(setq package-enable-at-startup nil)
(setq package-install-upgrade-built-in t)
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
(setq package-check-signature 'allow-unsigned)
(setq package-archive-contents nil)
(package-initialize)
(advice-add 'package-refresh-contents :override
            (lambda (&rest _)
              (message "Package refresh skipped (run M-x list-packages to refresh archives)"))
            '((name . no-refresh-on-init)))
(setq byte-compile-warnings '(cl-functions))
(use-package cl-lib)
(let ((default-directory  "~/.emacs.d/"))
  (normal-top-level-add-subdirs-to-load-path))
(add-to-list 'load-path "~/.emacs.d/lisp/")
;;-----------------------------------INTERFACE-----------------------------
;; (global-auto-remove-mode t)
(use-package diminish) ;; hides some minor mode line indicators
(use-package general) ;; simplify keybindings
(use-package recentf ;; recent files first
    :hook (after-init . recentf-mode)
    :custom (recentf-max-saved-items 100))
;; (use-package vertico ;;minibuffer completion
;;   :ensure t
;;   :init (vertico-mode)
;;   :bind (:map minibuffer-local-map
;;               ("<next>" . vertico-next-group)
;;               ("<prior>" . vertico-previous-group)))
(use-package orderless ;; multicomponent search filters
    :custom
  (completion-styles '(orderless basic))
  (completion-category-defaults nil)
  (completion-pcm-leading-wildcard t)
  (completion-category-overrides '((file (styles partial-completion)))))
(use-package marginalia ;;enhance minibuffer completion 
    :init
  (marginalia-mode 1))
;; (use-package treemacs ;; tree navigator
;;     :ensure t
;;     :bind ("<f5>" . treemacs)
;;     :custom (treemacs-is-never-other-windows)
;;     :hook (treemacs-mode . treemacs-project))
;; (use-package golden-ratio ;; increase active buffer
;;     :ensure t
;;     :hook (after-init . golden-ratio-mode)
;;     :custom (golden-ratio-exclude-modes '(occur-mode))
;;     (setq golden-ratio-adjust-factor 1
;; 	  golden-ratio-wide-adjust-factor 1)
;;     )
;; (use-package projectile) ;;features on project level without external dependencies
;; (projectile-mode +1)
(use-package transient ;; for magit
    :straight (:host github :type git :repo "magit/transient" :branch "main" ))
(use-package magit ;; git integration
    :straight (:host github :type git :repo "magit/magit" :branch "main" ))
;;-----------------------------------MODES-----------------------------
;;(require 'org-babel)
;; M-x customize-variable RET org-babel-load-languages
(use-package markdown-table-wrap)
(use-package org-roam ;;nodes and links in notes
    :ensure t
    :custom (org-roam-directory "~/lav/src/spiega/")
    :bind (("C-c n l" . org-roam-buffer-toggle)
	   ("C-c n f" . org-roam-node-find)
	   ("C-c n c" . org-roam-capture)
	   ("C-c n i" . org-roam-node-insert))
    :init (setq org-roam-v2-ack t)
    :custom(
	    (org-roam-setup)
	    (org-roam-db-autosync-mode)
	    (org-roam-db-sync))
    :config ()
    )
;; (use-package denote-roam ;;id for nodes
;;   :vc (:url "https://github.com/BardofSprites/denote-roam"
;;        :rev newest)
;;   :after (denote org-roam)
;;   :bind
;;   ("C-c n i" . denote-roam-insert-or-create-node)  ; node insert
;;   ("C-c n o" . denote-roam-find-or-create-node)    ; node open
;;   :custom
;;   ;; default is nil to include denote-journal entries in org-roam database
;;   (denote-roam-include-journal nil)
;;   (denote-roam-directory "~/Notes")
;;   :config
;;   (denote-roam-mode t))
(use-package org-roam-ui ;; graph browser 
    :straight (:host github :type git :repo "org-roam/org-roam-ui" :branch "main" :files ("*.el" "out"))
    :after org-roam
    ;;  :hook (after-init . org-roam-ui-mode)
    :config
    (setq org-roam-ui-sync-theme t
          org-roam-ui-follow t
          org-roam-ui-update-on-save t
          org-roam-ui-open-on-start nil))
(setq org-roam-file-extensions '("org" "md")) ;
(setq org-directory "~/lav/src/spiega/")
(add-to-list  'load-path "~/lav/src/spiega/")
(use-package md-roam
    :straight (:host github :type git :repo "nobiot/md-roam" :files ("*el"))
    :config
    (setq md-roam-file-extension "md")
    )
(md-roam-mode 1) ; md-roam-mode must be active before org-roam-db-sync
(setq org-capture-templates ;; C-c c: creates a link for agenda
      '(("t" "Todo" entry (file+headline "~/lav/src/spiega/project/agenda.org" "Tasks")
         "* TODO %?\n  %i\n  %a")
        ("j" "journal" entry (file+olp+datetree "~/lav/src/spiega/project/journal.org")
         "* %?\nEntered on %U\n  %i\n  %a")
        ("e" "emacs" entry (file+olp+datetree "~/lav/src/spiega/markdown/emacs.org")
         "* %?\nEntered on %U\n  %i\n  %a")
	("m" "Meeting" entry (file+headline "" "Meetings")
	 "* %?\n %U")
	("a" "Appointment" entry (file "personal/gcal.org")
         "* %?\n :PROPERTIES:\n :calendar-id: me@gmail.com\n :END:\n:org-gcal:\n%^T--%^T\n:END:\n"
	 :jump-to-captured t)
	("d" "Due Date" entry &rest (file "personal/gcal.org")
	 "* %?\n :PROPERTIES:\n :calendar-id: me@gmail.com\n :END:\n:org-gcal:\n%^T\n:END:\n")
	("w" "Task" entry (file ,(concat user-notes-dir "tasks/chores.org")
			   "* %?\nSCHEDULED: %^t\n%a" :empty-lines 1 :prepend t))
	("l" "Log" item (file+olp ,(concat user-notes-dir "personal/notes.org") "Log")
	 "- %U %?" :empty-lines-after 1)
	("t" "Team log" item (function org-team-visit-person-log)
	 "- %U %?" :prepend t)
	("b" "Book log" item (function org-books-visit-book-log)
	 "- %U %?" :prepend t)
	("s" "sysadmin" entry (file+olp+datetree "~/lav/src/spiega/markdown/sysadmin.org")
         "* %?\nEntered on %U\n  %i\n  %a")))
(add-to-list 'org-roam-capture-templates
	     '("m" "Markdown" plain "" :target
               (file+head "%<%Y-%m-%dT%H%M%S>.md"
		"---\ntitle: ${title}\nid: %<%Y-%m-%dT%H%M%S>\ncategory: \n---\n")
	       :unnarrowed t))
;; (use-package tikz)
;; (add-to-list 'org-latex-packages-alist
;;              '("" "tikz" t))
;; (add-to-list 'org-latex-packages-alist
;;              '("" "tikz-cd" t))
(use-package ox-hugo)
(use-package ox-reveal)
(use-package mathjax)
;;(setq org-reveal-root "https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/")
(setq org-reveal-root "../reveal/")
(setq org-re-reveal-root "../reveal/")
;;(setq org-reveal-external-plugins '((RevealMenu . "{ src: '../reveal/js/head.js', async: true, condition: function() { return !!document.body.classList; } },")))

(setq org-reveal-hlevel 1)
(use-package oer-reveal)
(setq oer-reveal-publish-org-publishing-functions
      '(oer-reveal-publish-to-reveal))
;;(setq oer-reveal--attribution-strings )

(defun roam-sitemap (title list)
  (concat "#+OPTIONS: ^:nil author:nil html-postamble:nil\n"
          "#+SETUPFILE: ./simple_inline.theme\n"
          "#+TITLE: " title "\n\n"
          (org-list-to-org list) "\nfile:sitemap.svg"))

(setq my-publish-time 0)   ; see the next section for context
(defun roam-publication-wrapper (plist filename pubdir)
  (org-roam-graph)
  (org-html-publish-to-html plist filename pubdir)
  (setq my-publish-time (cadr (current-time))))
(defun org-roam-custom-link-builder (node)
  (let ((file (org-roam-node-file node)))
    (concat (file-name-base file) ".html")))
(setq org-roam-graph-link-builder 'org-roam-custom-link-builder)
(setq org-publish-project-alist
      '(("blender_twin"
	 :base-directory "~/lav/src/spiega"
	 :publishing-directory "~/lav/siti/spiega/a/"
	 ;;:base-extension "org"
	 ;;:publishing-function org-html-publish-to-html
	 :publishing-function roam-publication-wrapper
	 :recursive t
	 ;;:include ("knowledge_base/*.md")
	 ;;:publishing-function my-org-publish-split-headings
	 :auto-sitemap t
	 :sitemap-function roam-sitemap
	 :sitemap-sort-files alphabetically
	 :sitemap-title "Roam notes"
         :section-numbers nil
         :with-toc nil
         :html-preamble t
         :html-postamble t
         :auto-sitemap t
	 :table-of-contents nil
         :sitemap-filename "sitemap.org"
         :sitemap-title "sitemap"
	 :style "<link rel=\"stylesheet\" href=\"../other/mystyle.cs\" type=\"text/css\">"
	 :html-head "<link rel=\"stylesheet\" href=\"static//css/org.css\" type=\"text/css\"/>\n"
         ;;:sitemap-function my-sitemap-format
	 )
        ("images"
         :base-directory "~/lav/src/spiega/img/"
         :base-extension "jpg\\|gif\\|png\\|svg"
         :recursive t
	 :publishing-directory "~/lav/siti/f/"
         :publishing-function org-publish-attachment)
        ("blog" ;; Meta-project to combine phases
         :components ("blender_twin" "images"))))

;; (use-package denote ;;namespace and metadata for files
;;   :ensure t
;;   :hook (dired-mode . denote-dired-mode)
;;   :bind
;;   (("C-c n n" . denote)
;;    ("C-c n r" . denote-rename-file)
;;    ("C-c n l" . denote-link)
;;    ("C-c n b" . denote-backlinks)
;;    ("C-c n d" . denote-dired)
;;    ("C-c n g" . denote-grep))
;;   :config
;;   (setq denote-directory (expand-file-name "~/lav/src/spiega/markdown/"))
;;   (denote-rename-buffer-mode 1))
(use-package deft
    :after org
    :bind
    ("C-c n d" . deft)
    :custom
    (deft-recursive t)
    (deft-use-filter-string-for-filename t)
    (deft-default-extension "org")
    (deft-directory org-roam-directory))
;;---------------------------------------Org-mode-settings-----------------------------------
(use-package ob-async) ;; bash org in background
(use-package org
    ;; :straight (:type built-in)
    :hook ((org-mode . visual-line-mode))
    :config
    (setq org-startup-indented t
          org-hide-emphasis-markers t
          org-return-follows-link t
          org-log-done 'time
	  org-startup-truncated nil
	  org-confirm-babel-evaluate nil
	  org-display-inline-images t
	  org-adapt-indentation nil
	  org-startup-indented nil
	  org-export-body-only t
	  org-src-fontify-natively t
	  org-startup-folded t ;; Fold headers
	  org-startup-with-inline-images t ;; Show inline images, may blow up the screen
	  org-image-actual-width nil ;; Lets you set your own image width
	  ;;org-agenda-include-diary t
          org-edit-src-content-indentation 0))
(use-package org-journal ;; journal entries
    :bind
  ("C-c n j" . org-journal-new-entry)
  :custom
  (org-journal-date-prefix "#+title: ")
  (org-journal-file-format "%Y-%m-%d.org")
  (org-journal-dir "~/lav/src/spiega/org/")
  (org-journal-date-format "%A, %d %B %Y"))

(use-package org-download ;;copy and paste images ;; apt install wl-clipboard
    :after org
    :bind
    (:map org-mode-map
          (("s-Y" . org-download-screenshot)
           ("s-y" . org-download-yank))))
(setq-default org-download-image-dir "~/lav/siti/f/f_twin/")
(setq-default truncate-lines nil)
(org-babel-do-load-languages
 'org-babel-load-languages
 '(
   (shell . t)
   (python . t)
   (dot . t)
   (sql . t)
   (sqlite . t)
   (R . t)
   (sql . t)
   (gnuplot . t)
   (lilypond . t)
   (haskell . t)
   (scheme . t) ;; Here is where you can list what languages you want syntax highlighting for
   (latex . t)
   )
 )
(setq org-export-body-only t)
(setq org-html-validation-link nil)
;;(org-agenda nil "a") load agenda at startup
(use-package org-super-agenda)

(setq org-agenda-custom-commands
      '(("d" "Today's Tasks"
	 ((agenda "" ((org-agenda-span 1)
		      (org-agenda-overriding-header "Today's Tasks")))))))
(setq org-agenda-custom-commands
      '(
	("r" "Today's Agenda"
	 ((agenda ""
		  ((org-agenda-block-separator ?*) ;; Makes the separator *'s
		   (org-agenda-span 1) ;; Lists items scheduled or deadlined for today
		   (org-agenda-format-date "")
		   (org-agenda-files '("~/emacs/planner/college")) ;; Specify folder the .org files are in
		   (org-agenda-overriding-header "School"))) ;; Title of header
	  (agenda ""
		  ((org-agenda-block-separator ?*)
                   (org-agenda-span 1)
                   (org-agenda-format-date "")
                   (org-agenda-files '("~/emacs/planner/work"))
                   (org-agenda-overriding-header "\nWork")))
	  (agenda ""
		  ((org-agenda-block-separator ?*)
                   (org-agenda-span 90)
                   (org-agenda-entry-types '(:deadline)) ;; Show only deadlines
                   (org-agenda-show-all-dates nil)
                   (org-agenda-files '("~/emacs/planner/college" "~/emacs/planner/work"))
                   (org-agenda-overriding-header "\nAll Upcoming\n")))
          ))
	("w" "Week's Agenda"
	 ((agenda ""
		  ((org-agenda-block-separator ?*)
                   (org-agenda-span 7)
                   (org-agenda-files '("~/emacs/planner/college" "~/emacs/planner/work"))
		   ))
	  ))
	("q" "Week's Deadlines"
	 ((agenda ""
		  ((org-agenda-block-separator ?*)
                   (org-agenda-span 7)
                   (org-agenda-entry-types '(:deadline))
                   (org-agenda-files '("~/emacs/planner/college" "~/emacs/planner/work"))
		   ))
	  ))
	))

(let ((org-super-agenda-groups
       '(
         (:name "Today"  
          :time-grid t  
          :todo "TODAY")  
         (:name "Important"
          :tag "bills"
          :priority "A")
         (:order-multi (2 (:name "Shopping in town"
                                 :and (:tag "shopping" :tag "@town"))
                        (:name "Food-related"
                               :tag ("food" "dinner"))
                        (:name "Personal"
                               :habit t
                               :tag "personal")))
         (:todo "WAITING" :order 8)  ; Set order of this section
         (:todo ("SOMEDAY" "TO-READ" "CHECK" "TO-WATCH" "WATCHING")
          :order 9)
         (:priority<= "B"
          :order 1)
         )))
  (org-agenda nil "a"))
;;(setq org-agenda-files directory-files-recursively org-directory "\\.org")
(require 'ox-publish)
(use-package ob-mermaid) ;; graph
(setq ob-mermaid-cli-path "/snap/bin/mermaid-cli.mmdc")
(use-package graphviz-dot-mode ;;graph
    :ensure t
    :config
    (setq graphviz-dot-indent-width 4)
    :hook
    (graphviz-dot-mode . flycheck-mode))

(setq org-publish-project-alist
      (list
       (list "org-site:main"
             :recursive t
             :base-directory "./content"
             :publishing-function 'org-html-publish-to-html
             :publishing-directory "./public"
             :with-author nil           ;; Don't include author name
             :with-creator t            ;; Include Emacs and Org versions in footer
             :with-toc t                ;; Include a table of contents
             :section-numbers nil       ;; Don't include section numbers
	     :org-export-body-only t    ;; no headers
             :time-stamp-file nil)))    ;; Don't include time stamp in file
;;;---------------------------------------autocompletion--------------------------------------
(use-package corfu ;; autocompletion
  ;; :hook ((prog-mode . (lambda () (setq-local corfu-auto)))
  ;;        (shell-mode . corfu-mode)
  ;;        (eshell-mode . corfu-mode))
  :init
  (global-corfu-mode)
  )
(use-package emacs
  :custom
  (tab-always-indent 'complete)
  (text-mode-ispell-word-completion nil)
  (read-extended-command-predicate #'command-completion-default-include-p)
  (read-extended-command-predicate #'command-completion-default-include-p))
(use-package dabbrev ;; autocompletion
    ;; Swap M-/ and C-M-/
    :bind (("M-/" . dabbrev-completion)
           ("C-M-/" . dabbrev-expand))
    :config
    (add-to-list 'dabbrev-ignored-buffer-regexps "\\` ")
    (add-to-list 'dabbrev-ignored-buffer-modes 'authinfo-mode)
    (add-to-list 'dabbrev-ignored-buffer-modes 'doc-view-mode)
    (add-to-list 'dabbrev-ignored-buffer-modes 'pdf-view-mode)
    (add-to-list 'dabbrev-ignored-buffer-modes 'tags-table-mode))
;; (use-package company ;; classic autocompletion
;;     :config
;;   (define-key company-active-map (kbd "M-.") #'company-show-location)
;;   (define-key company-active-map (kbd "RET") nil)
;;   )
;; (defun company-jedi-initialize ()
;;   "To prevent an ERROR."
;;   ())
;; (defun my/python-mode-hook ()
;;   (add-to-list 'company-backends 'company-jedi))
;; (use-package company-jedi
;;   :ensure t
;;   :config
;;   (add-hook 'python-mode-hook 'company-jedi-initialize))
;; (add-hook 'python-mode-hook 'my/python-mode-hook)
;; (add-to-list 'company-backends '(company-jedi company-files))
;; (use-package helm ;;display completion
;;     :straight t
;;     :config
;;     )
;;(use-package ivy ;;dispay completion
;;)
(setq find-file-visit-truename t)
;;------------------------------language-modes------------------------------
(use-package json)
(defun beautify-json ()
  (interactive)
  (let ((b (if mark-active (min (point) (mark)) (point-min)))
        (e (if mark-active (max (point) (mark)) (point-max))))
    (shell-command-on-region b e
			     "python -mjson.tool" (current-buffer) t)))
;; ESS (R)
(when (use-package ess)
  (add-to-list 'auto-mode-alist '("\\.R\\'" . ess-r-mode))
  (add-hook 'ess-mode-hook
            (lambda ()
              (local-set-key (kbd "RET") 'newline)))
  (setq ess-indent-with-fancy-comments nil))
;; Web mode
(when (use-package web-mode)
  (add-to-list 'auto-mode-alist '("\\.phtml\\'" . web-mode))
  (add-to-list 'auto-mode-alist '("\\.ts\\'" . web-mode))
  (add-to-list 'auto-mode-alist '("\\.js\\'" . web-mode))
  (add-to-list 'auto-mode-alist '("\\.ts\\'" . web-mode))
  (add-to-list 'auto-mode-alist '("\\.css\\'" . web-mode))
  (add-to-list 'auto-mode-alist '("\\.php\\'" . web-mode))
  (add-to-list 'auto-mode-alist '("\\.html?\\'" . web-mode))
  )
(when (use-package web-beautify)
  (eval-after-load 'js2-mode '(define-key js2-mode-map (kbd "C-c b") 'web-beautify-js))
  (eval-after-load 'js '(define-key js-mode-map (kbd "C-c b") 'web-beautify-js))
  (eval-after-load 'json-mode '(define-key json-mode-map (kbd "C-c b") 'web-beautify-js))
  (eval-after-load 'sgml-mode '(define-key html-mode-map (kbd "C-c b") 'web-beautify-html))
  (eval-after-load 'css-mode '(define-key css-mode-map (kbd "C-c b") 'web-beautify-css)))
(when (require 'yaml-mode nil t)
  (add-hook 'yaml-mode-hook
            (lambda ()
              (define-key yaml-mode-map "\C-m" 'newline-and-indent))))
(require 'php-mode nil t)
;;------------------------------------BACKUP--------------------------------
(desktop-save-mode 1)
(setq desktop-path '("~/.emacs.d/"))
(setq desktop-dirname "~/.emacs.d/")
(setq desktop-base-file-name "desktop")
(setq desktop-save t)                     ; always save without asking
(setq desktop-save-ask-if-new nil)        ; don't ask when creating/saving desktop file
(setq desktop-load-locked-desktop t)      ; load even if locked (crashed session)
(setq desktop-restore-eager 0)            ; 0 = restore buffers lazily (avoids blocking on heavy modes at startup)
(setq confirm-kill-processes nil)        ; don't ask "kill processes and exit?" — just exit (yes by default)
(custom-set-variables '(org-agenda-files (quote ("~/lav/src/spiega/project/agenda.org"))))
;; C-x C-s: save without asking "make it writable?" when buffer is read-only
(advice-add 'save-buffer :before
            (lambda (&rest _) (when buffer-read-only (setq buffer-read-only nil)))
            '((name . my-save-unlock-readonly)))
(custom-set-variables
 '(auto-save-file-name-transforms '((".*" "~/.emacs.d/saves/\\1" t)))
 '(backup-directory-alist '((".*" . "~/.emacs.d/backups/"))))
;; Paths under these prefixes skip "file changed" / "Reread from disk?" (something on the mount triggers false positives).
(defvar my-skip-file-changed-check-prefixes '("/home/sabeiro/mount/")
  "List of path prefixes (strings). For files under these, never prompt 'file changed' / 'Reread from disk?'.
Customize if your mount is elsewhere, e.g. (setq my-skip-file-changed-check-prefixes '(\"/mnt/nfs\"))")
(defun my-file-under-skip-change-check-p (filename)
  (and filename
       (boundp 'my-skip-file-changed-check-prefixes)
       my-skip-file-changed-check-prefixes
       (let ((expanded (expand-file-name filename)))
         (cl-some (lambda (prefix) (string-prefix-p (expand-file-name prefix) expanded))
                  my-skip-file-changed-check-prefixes))))
;; "File changed on disk. Reread?" — skip for paths in my-skip-file-changed-check-prefixes; else default (timestamp).
(advice-add 'ask-user-about-supersession-threat :around
            (lambda (orig fn)
              (if (my-file-under-skip-change-check-p fn)
                  nil
                  (funcall orig fn)))
            '((name . my-supersession-skip-mount-paths)))
;; "Save anyway?" — skip for paths in my-skip-file-changed-check-prefixes; else use normal timestamp check.
(advice-add 'verify-visited-file-modtime :around
            (lambda (orig &rest args)
              (if (my-file-under-skip-change-check-p (buffer-file-name))
                  nil
                  (apply orig args)))
            '((name . my-verify-modtime-skip-mount-paths)))

(setq
 backup-by-copying t      ; don't clobber symlinks
 backup-directory-alist
 '(("." . "~/.emacs.d/saves/"))    ; don't litter my fs tree
 delete-old-versions t
 kept-new-versions 6
 kept-old-versions 2
 version-control t) 
(setq temporary-file-directory "~/lav/tmp/")
(setq small-temporary-file-directory "~/lav/tmp/")
;; misc keybindings
;; (define-key isearch-mode-map (kbd "<left>") 'isearch-repeat-backward)
;; (global-set-key (kbd "<f4>") (lambda () (interactive) (setq current-prefix-arg '(4)) (call-interactively 'compile)))
;; (setq backup-directory-alist
;;      `((".*" . ,temporary-file-directory)))
;; (setq auto-save-file-name-transforms
;;      `((".*" ,temporary-file-directory t)))

;; utility functions
;; (defun join-lines (arg)
;;   (interactive "p")
;;   (end-of-line)
;;   (delete-char 1)
;;   (delete-horizontal-space)
;;   (insert " "))
;; (defun concat-lines ()
;;   (interactive)
;; (next-line)
;;   (join-line)
;;   (delete-horizontal-space))
;;-----------------------------------coding-assistant----------------------------
;; built-in: dabbrev, hippie-expand, completion-at-point. Extensions: company corfu minuet 
(use-package dumb-jump ;; jump to definition
  :ensure t
  :custom
  (dumb-jump-prefer-searcher 'rg)
  (xref-show-definitions-function #'consult-xref)
  :config
  (add-hook 'xref-backend-functions #'dumb-jump-xref-activate))

(when (use-package minuet) ;; autocompletion
  (setq minuet-provider 'openai-fim-compatible)
  (setq minuet-n-completions 1)
  (setq minuet-context-window 512)
  (setq minuet-auto-suggestion-debounce-delay 0.5)
  (setq minuet-auto-suggestion-throttle-delay 1.0)
  ;;(plist-put minuet-openai-fim-compatible-options :end-point "https://ollama.jetson/v1/completions")
  (plist-put minuet-openai-fim-compatible-options :end-point "http://localhost/v1/completions")
  (plist-put minuet-openai-fim-compatible-options :name "Ollama")
  (plist-put minuet-openai-fim-compatible-options :api-key "TERM")
  (plist-put minuet-openai-fim-compatible-options :model "qwen2.5-coder:3b")
  (minuet-set-optional-options minuet-openai-fim-compatible-options :max_tokens 56)
  (with-eval-after-load 'minuet
    (when (and (boundp 'minuet-active-mode-map)
               (keymapp (symbol-value 'minuet-active-mode-map)))
      (let ((map minuet-active-mode-map))
        (define-key map (kbd "M-a") #'minuet-accept-suggestion-line)
        (define-key map (kbd "M-A") #'minuet-accept-suggestion)
        (define-key map (kbd "M-e") #'minuet-dismiss-suggestion)
        (define-key map (kbd "M-n") #'minuet-next-suggestion)
        (define-key map (kbd "M-p") #'minuet-previous-suggestion)
        (define-key map (kbd "<tab>") #'minuet-accept-suggestion-line)))
    (global-set-key (kbd "M-i") 'minuet-show-suggestion)
    (global-set-key (kbd "M-y") 'minuet-complete-with-minibuffer)))
;;-----------------------------------interactive-coding----------------------------
;; Lisp: ensure startup buffer and .el/.elc files use a Lisp mode
(setq initial-major-mode 'lisp-interaction-mode)
(add-to-list 'auto-mode-alist '("\\.el\\'" . lisp-mode))
(add-to-list 'auto-mode-alist '("\\.elc\\'" . lisp-mode))
(add-hook 'find-file-hook
          (lambda ()
            (when (and (buffer-file-name) (string-match "\\.elc?\\'" (buffer-file-name)))
              (lisp-mode))))
;; (autoload 'python-mode "python-mode" "Python Mode." t)
(add-to-list 'auto-mode-alist '("\\.py\\'" . company-mode))
(add-to-list 'auto-mode-alist '("\\.py*\\'" . python-mode))
(add-to-list 'interpreter-mode-alist '("python" . python-mode))
(setq python-shell-interpreter "/usr/bin/python3"
      python-shell-interpreter-args "-i")
(setq py-python-command "/usr/bin/python3")
(defun my-python-auto-run ()
  "Start inferior Python process if not already running (stays in current buffer)."
  (when (fboundp 'python-shell-get-process)
    (unless (python-shell-get-process)
      (let ((cur (current-buffer)))
        (run-python)
        (switch-to-buffer cur)))))

;; (use-package bind-key)
(add-hook 'python-mode-hook
          (lambda ()
            (my-python-auto-run)
            (local-set-key (kbd "C-a") #'python-shell-send-region)
            (local-set-key (kbd "<C-return>") #'python-shell-send-region)
            (local-set-key (kbd "C-m") #'newline-and-indent)))
;; (use-package blacken
;;     :ensure t
;;     :hook (python-mode . gopar/enable-blacken-if-found)
;;     :init
;;     (defun gopar/enable-blacken-if-found ()
;;       "format the buffer using bleken if found"
;;       (interactive)
;;       (if (executable-find "black")
;; 	  (blacken-mode)
;; 	  (message "Black not found"))))
;;-----------------------------------LLM-----------------------------
(use-package ollama-buddy
  :ensure t
  :custom (ollama-buddy-default-model "qwen3.5:9b")
  :bind
  ("C-c o" . ollama-buddy-role-transient-menu)
  ("C-c O" . ollama-buddy-transient-menu))
(setq ollama-buddy-unsloth-api-key (getenv "UNSLOTH_TOKEN"))
(setq ollama-buddy-host "localhost")
(setq ollama-buddy-port 11434)
(setq ollama-buddy-convert-markdown-to-org t)
(setq ollama-buddy-streaming-enabled t)
(setq ollama-buddy-auto-scroll t)
(setq ollama-buddy-max-file-size (* 10 1024 1024))  ; 10MB
(use-package md-ts-mode)
;; (use-package pi-coding-agent)

;; (use-package pi-coding-agent ;;coding assistant
;;     :ensure t
;;     :init (defalias 'pi 'pi-coding-agent)
;;     :custom
;;     (pi-coding-agent-input-window-height 10); Height of input window
;;     (pi-coding-agent-tool-preview-lines 10); Lines shown before collapsing tool output
;;     (pi-coding-agent-bash-preview-lines 5); Lines shown for bash output
;;     (pi-coding-agent-context-warning-threshold 70)  ; Warn when context exceeds this %
;;     (pi-coding-agent-context-error-threshold 90); Critical when context exceeds this %
;;     (pi-coding-agent-visit-file-other-window t); RET opens file in other window (nil for same)
;;     (pi-coding-agent-hot-tail-turn-count 3); Recent headed turns that re-wrap on resize
;;     ;; (pi-coding-agent-thinking-display 'hidden); Collapse completed thinking by default
;;     ;; (pi-coding-agent-thinking-hidden-preview nil); Always use generic "Thinking hidden…" stubs
;;     ;; (pi-coding-agent-copy-raw-markdown t)            ; Keep raw markdown on copy (default: strip hidden markup)
;;     ;; (pi-coding-agent-input-markdown-highlighting nil) ; Plain text input buffer
;;     )
;; (use-package vterm :ensure t)
(defvar gptel-tools-dir user-emacs-directory
  "Directory containing gptel_tools.el and other gptel support files.")
(defun gptel-load-and-call ()
  "Load gptel, backends, and gptel_tools on first use; then run gptel."
  (interactive)
  (add-to-list 'load-path gptel-tools-dir)
  (use-package gptel_tools
    :straight nil)
  (unless (featurep 'gptel)
    (global-set-key (kbd "C-c C-g") 'gptel-send))
  (call-interactively 'gptel))
(define-key org-mode-map (kbd "C-c C-b") #'my/gptel-blender-prompt)
(global-set-key (kbd "C-c g") 'gptel-load-and-call)
(defun ellama-load-and-call ()
  "Load ellama, backends, and ellama_tools on first use;"
  (interactive)
  (add-to-list 'load-path gptel-tools-dir)
  (use-package ellama_setup
    :straight nil))
;;-----------------------------------JS/NODE-----------------------------
(use-package htmlize)
(when (use-package nodejs-repl)
  (setq inferior-js-program-command "node --interactive")
  (defun my-node-compile ()
    (interactive)
    (shell)
    (goto-char (point-max))
    (comint-kill-input)
    (insert "npm run build --prefix .")
    (comint-send-input))
  (add-hook 'js-mode-hook
            (lambda ()
              (define-key js-mode-map (kbd "C-x C-e") 'nodejs-repl-send-last-expression)
              (define-key js-mode-map (kbd "C-c C-j") 'nodejs-repl-send-line)
              (define-key js-mode-map (kbd "C-a") 'nodejs-repl-send-region)
              (define-key js-mode-map (kbd "C-c C-l") 'nodejs-repl-load-file)
              (define-key js-mode-map (kbd "C-c C-c") 'my-node-compile)
              (define-key js-mode-map (kbd "C-c C-z") 'nodejs-repl-switch-to-repl)))
  )
;; `python-shell-interpreter-interactive-arg' or add regexps
;; matching shell prompts in the directory-local friendly vars:
;;   + `python-shell-prompt-regexp'
;;   + `python-shell-prompt-block-regexp'
;;   + `python-shell-prompt-output-regexp'
;; Or alternatively in:
;;   + `python-shell-prompt-input-regexps'
;;   + `python-shell-prompt-output-regexps'
;;-----------------------------------PLATFORMIO-----------------------------
;;(add-to-list 'projectile-project-root-files "platformio.ini")
(when (use-package platformio-mode)
  (add-hook 'c-mode-hook
            (lambda ()
              (when (locate-dominating-file default-directory "platformio.ini")
                (platformio-conditionally-enable)))))
;; Keybindings for PlatformIO: C-c i b build, C-c i u upload, C-c i s serial, C-c i c clean
;;-----------------------------------SPELLING-----------------------------
;; Auto-detect hunspell or aspell
(cond
  ((executable-find "hunspell")
   (setq ispell-program-name "hunspell")
   (ispell-set-spellchecker-params)
   (setq ispell-local-dictionary "en_US,it_IT")
   (ispell-hunspell-add-multi-dic "en_GB,it_IT")
   (setq ispell-local-dictionary-alist
         '(("en_US" "[[:alpha:]]" "[^[:alpha:]]" "[']" nil ("-d" "en_US") nil utf-8))))
  ((executable-find "aspell")
   (setq ispell-program-name "aspell")
   (setq ispell-extra-args '("--sug-mode=ultra" "--lang=en_US"))))
;; Enable flyspell for text and markdown modes
(add-hook 'text-mode-hook 'flyspell-mode)
;; For markdown, use flyspell but skip code blocks and URLs
(add-hook 'markdown-mode-hook
          (lambda ()
            (setq flyspell-generic-check-word-predicate
                  (lambda ()
                    (not (or (markdown-code-block-at-point-p)
                             (markdown-inline-code-at-point-p)
                             (markdown-link-p)))))
            (flyspell-mode 1)))
;;-----------------------------------Multimedia-----------------------------
(use-package lilypond)
;;(require 'lilypond-mode)
(autoload 'LilyPond-mode "lilypond-mode" "LilyPond Editing Mode" t)
(add-to-list 'auto-mode-alist '("\\.ly$" . LilyPond-mode))
(add-to-list 'auto-mode-alist '("\\.ily$" . LilyPond-mode))
(add-hook 'LilyPond-mode-hook (lambda () (turn-on-font-lock)))
(add-hook 'LilyPond-mode-hook (function (lambda () (add-to-list 'LilyPond-command-alist '("OpenPDF" "open '%f'")))))
(defvar ac-lilypond-identifiers
  '((candidates . (lambda () (all-completions ac-target LilyPond-identifiers)))))
;;(defvar ni-LilyPond-keywords (mapcar (lambda (x) (concat "\\" x)) LilyPond-keywords))
(defvar ac-lilypond-keywords
  '((candidates . (lambda () (all-completions ac-target ni-LilyPond-keywords)))))
(defvar ac-lilypond-Creserved-words
  '((candidates . (lambda () (all-completions ac-target LilyPond-Capitalized-Reserved-Words)))))
(defvar ac-lilypond-ncreserved-words
  '((candidates . (lambda () (all-completions ac-target LilyPond-non-capitalized-reserved-words)))))
;;(provide 'init-lilypond)
;;(provide 'init)
;;; init.el ends here
