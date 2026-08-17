;; (require 'epa-file)
;; (epa-file-enable)
(require 'org-roam)
(require 'org-roam-ui)
(require 'ox-reveal)
(require 'ox-ipynb)
(add-hook 'org-mode-hook (lambda () (setq truncate-lines nil)));
(setq org-startup-indented t)

(with-eval-after-load 'org
  (set-face-attribute 'org-table nil :inherit 'fixed-pitch)
  (set-face-attribute 'org-code nil :inherit 'fixed-pitch)
  (set-face-attribute 'org-verbatim nil :inherit 'fixed-pitch))

(org-babel-do-load-languages
 'org-babel-load-languages
 '((C . t)
   (R . t)
   (emacs-lisp . t)
   (java . t)
   (lilypond . t)
   (plantuml . t)
   (python . t)
   (ruby . t)
   (sql . t)))

(when (executable-find "jupyter")
  (org-babel-do-load-languages
   'org-babel-load-languages
   '((jupyter . t)))
  (define-key jupyter-org-interaction-mode-map (kbd "C-s-c h") #'jupyter-org-hydra/body)
  (define-key jupyter-org-interaction-mode-map (kbd "C-c h") nil))

(setq org-plantuml-jar-path-linux "/usr/share/plantuml/plantuml.jar")
(when (file-exists-p org-plantuml-jar-path-linux)
  (custom-set-variables '(org-plantuml-jar-path org-plantuml-jar-path-linux)))

(cl-defmethod org-roam-node-slug ((node org-roam-node))
  "Return the slug of NODE."
  (let ((title (org-roam-node-title node))
        (slug-trim-chars '(768 769 770 771 772 774 775 776 777 778 779 780 795 803 804 805 807 813 814 816 817)))
    (cl-flet* ((nonspacing-mark-p (char) (memq char slug-trim-chars))
               (strip-nonspacing-marks (s) (string-glyph-compose
                                            (apply #'string
                                                   (seq-remove #'nonspacing-mark-p
                                                               (string-glyph-decompose s)))))
               (cl-replace (title pair) (replace-regexp-in-string (car pair) (cdr pair) title)))
      (let* ((pairs `(("[^[:alnum:][:digit:]]" . "-") ;; convert anything not alphanumeric
                      ("--*" . "-")                   ;; remove sequential hyphens
                      ("^-" . "")                     ;; remove starting hyphen
                      ("-$" . "")))                   ;; remove ending hyphen
             (slug (-reduce-from #'cl-replace (strip-nonspacing-marks title) pairs)))
        (downcase slug)))))

(defun org-roam-ui--make-graphdata ()
  "Get roam data and make JSON"
  (let* ((nodes-names
          [id
           file
           title
           level
           pos
           olp
           properties
           tags])
         (old (not (fboundp 'org-roam-db-map-citations)))
         (links-db-rows (if old
                            (org-roam-ui--separate-ref-links
                             (org-roam-ui--get-links old))
                          (seq-concatenate
                           'list
                           (org-roam-ui--separate-ref-links
                            (org-roam-ui--get-cites))
                           (org-roam-ui--get-links))))
         (links-with-empty-refs (org-roam-ui--filter-citations links-db-rows))
         (empty-refs (delete-dups (seq-map
                                   (lambda (link)
                                     (nth 1 link))
                                   links-with-empty-refs)))
         (nodes-db-rows (org-roam-ui--get-nodes))
         (fake-nodes (seq-map #'org-roam-ui--create-fake-node empty-refs))
         ;; Try to update real nodes that are reference with a title build
         ;; from their bibliography entry. Check configuration here for avoid
         ;; unneeded iteration though nodes.
         (retitled-nodes-db-rows (if org-roam-ui-retitle-ref-nodes
                                     (seq-map #'org-roam-ui--retitle-node
                                              nodes-db-rows)
                                   nodes-db-rows))
         (complete-nodes-db-rows (append retitled-nodes-db-rows fake-nodes))
         (response `((nodes . ,(mapcar
                                (apply-partially
                                 #'org-roam-ui-sql-to-alist
                                 (append nodes-names nil))
                                complete-nodes-db-rows))
                     (links . ,(mapcar
                                (apply-partially
                                 #'org-roam-ui-sql-to-alist
                                 '(source target type))
                                links-db-rows))
                     (tags . ,(seq-mapcat
                               #'seq-reverse
                               (org-roam-db-query
                                [:select :distinct tag :from tags]))))))
    (when old
      (message "[org-roam-ui] You are not using the latest version of org-roam.
This database model won't be supported in the future, please consider upgrading."))
    (json-encode
     `((type . "graphdata")
       (data . ,response)))))

(defun org-roam-ui--export-graphdata (file)
  "Create a JSON-file containting graphdata."
  (write-region (org-roam-ui--make-graphdata) nil file))

(defun org-roam-ui-export ()
  "Export `org-roam-ui's-data for usage as static webserver."
  (interactive)
  (let* ((dir (read-file-name "Specify output directory:"))
         (graphdata-file (concat (file-name-as-directory dir) "graphdata.json"))
         (notes-dir (concat (file-name-as-directory dir) "notes/")))
    (org-roam-ui--export-graphdata graphdata-file)
    (make-directory notes-dir :parents)
    (mapcar (lambda (id)
              (let* ((cid (car id))
                     (content (org-roam-ui--get-text cid)))
                (write-region content nil (concat notes-dir cid) 'append)))
            (org-roam-db-query "select id from nodes;"))))

(setq system-time-locale "C")
(setf (elt org-time-stamp-rounding-minutes 1) 1)
(setq org-time-stamp-formats '("<%Y-%m-%d %a>" . "<%Y-%m-%d %a %H:%M:%S>"))
(setq org-time-stamp-custom-formats '("<%Y-%m-%d %A>" . "<%Y-%m-%d %A %H:%M:%S>"))
(setq-default org-display-custom-times nil)
(setq org-roam-directory "~/work/repositories/org-roam")
(setq org-roam-capture-templates '(("d" "default" plain "%?"
                                    :if-new
                                    (file+head "${slug}.org"
                                               "#+title: ${title}\n#+author: x\n#+created: %<[%Y-%m-%d %a %H:%M:%S]>\n#+modified: %U\n\n")
                                    :immediate-finish t))
      time-stamp-active t
      time-stamp-start "#\\+modified: [\t]*"
      time-stamp-end "$"
      time-stamp-format "\[%Y-%m-%d %a %H:%M:%S\]")
(add-hook 'before-save-hook 'time-stamp nil)

(setq org-publish-project-alist
      '(("Bigblow"
         :base-directory "~/work/notebook/source"
         :base-extension "org"
         :publishing-directory "~/work/notebook/target"
         :publishing-function org-html-publish-to-html
         :auto-sitemap t
         :recursive t
         :sitemap-filename "index.org"
         :sitemap-title "Notebook"
         :sitemap-style tree
         :html-head-extra "
<link rel='stylesheet' type='text/css' href='https://xinii.github.io/org-html-themes/styles/bigblow/css/htmlize.css'/>
<link rel='stylesheet' type='text/css' href='https://xinii.github.io/org-html-themes/styles/bigblow/css/bigblow.css'/>
<link rel='stylesheet' type='text/css' href='https://xinii.github.io/org-html-themes/styles/bigblow/css/hideshow.css'/>
<script type='text/javascript' src='https://xinii.github.io/org-html-themes/styles/bigblow/js/jquery-1.11.0.min.js'></script>
<script type='text/javascript' src='https://xinii.github.io/org-html-themes/styles/bigblow/js/jquery-ui-1.10.2.min.js'></script>
<script type='text/javascript' src='https://xinii.github.io/org-html-themes/styles/bigblow/js/jquery.localscroll-min.js'></script>
<script type='text/javascript' src='https://xinii.github.io/org-html-themes/styles/bigblow/js/jquery.scrollTo-1.4.3.1-min.js'></script>
<script type='text/javascript' src='https://xinii.github.io/org-html-themes/styles/bigblow/js/jquery.zclip.min.js'></script>
<script type='text/javascript' src='https://xinii.github.io/org-html-themes/styles/bigblow/js/bigblow.js'></script>
<script type='text/javascript' src='https://xinii.github.io/org-html-themes/styles/bigblow/js/hideshow.js'></script>
<script type='text/javascript' src='https://xinii.github.io/org-html-themes/styles/lib/js/jquery.stickytableheaders.min.js'></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/pangu/4.0.7/pangu.js'></script>
<script> document.addEventListener('DOMContentLoaded', () => { pangu.autoSpacingPage(); }); </script>")
        ("ReadTheOrg"
         :base-directory "~/work/notebook/source"
         :base-extension "org"
         :publishing-directory "~/work/notebook/target"
         :publishing-function org-html-publish-to-html
         :auto-sitemap t
         :recursive t
         :sitemap-filename "index.org"
         :sitemap-title "Notebook"
         :sitemap-style tree
         :html-head-extra "
<link rel='stylesheet' type='text/css' href='https://xinii.github.io/org-html-themes/styles/readtheorg/css/htmlize.css'/>
<link rel='stylesheet' type='text/css' href='https://xinii.github.io/org-html-themes/styles/readtheorg/css/readtheorg.css'/>
<script src='https://xinii.github.io/org-html-themes/styles/lib/js/jquery.min.js'></script>
<script src='https://xinii.github.io/org-html-themes/styles/lib/js/bootstrap.min.js'></script>
<script src='https://xinii.github.io/org-html-themes/styles/lib/js/jquery.stickytableheaders.min.js'></script>
<script src='https://xinii.github.io/org-html-themes/styles/readtheorg/js/readtheorg.js'></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/pangu/4.0.7/pangu.js'></script>
<script> document.addEventListener('DOMContentLoaded', () => { pangu.autoSpacingPage(); }); </script>")
        ("html-norang"
         :base-directory "~/work/notebook/source"
         :base-extension "org"
         :publishing-directory "~/work/notebook/target"
         :publishing-function org-html-publish-to-html
         :auto-sitemap t
         :recursive t
         :sitemap-filename "index.org"
         :sitemap-title "Personal notebook"
         :sitemap-style tree
         :html-head-extra "
<link rel='stylesheet' type='text/css' href='https://ss1.xrea.com/xin.g2.xrea.com/content/org-style/norang.css'/>
<script src='https://cdnjs.cloudflare.com/ajax/libs/pangu/4.0.7/pangu.js'></script>
<script> document.addEventListener('DOMContentLoaded', () => { pangu.autoSpacingPage(); }); </script>")
        ("html-worg"
         :base-directory "~/work/notebook/source"
         :base-extension "org"
         :publishing-directory "~/work/notebook/target"
         :publishing-function org-html-publish-to-html
         :auto-sitemap t
         :recursive t
         :sitemap-filename "index.org"
         :sitemap-title "Personal notebook"
         :sitemap-style tree
         :html-head-extra "
<link rel='stylesheet' type='text/css' href='https://sambatriste.github.io/org-mode-theme-gallery/worg/worg.css'/>
<script src='https://cdnjs.cloudflare.com/ajax/libs/pangu/4.0.7/pangu.js'></script>
<script> document.addEventListener('DOMContentLoaded', () => { pangu.autoSpacingPage(); }); </script>")
        ("html-blank"
         :base-directory "~/work/notebook/source"
         :base-extension "org"
         :publishing-directory "~/work/notebook/target"
         :publishing-function org-html-publish-to-html
         :auto-sitemap t
         :recursive t
         :sitemap-filename "index.org"
         :sitemap-title "Personal notebook"
         :sitemap-style tree
         :html-head-extra "
<script src='https://cdnjs.cloudflare.com/ajax/libs/pangu/4.0.7/pangu.js'></script>
<script> document.addEventListener('DOMContentLoaded', () => { pangu.autoSpacingPage(); }); </script>")
        ("latex-article"
         :base-directory "~/work/notebook/source"
         :base-extension "org"
         :publishing-directory "~/work/notebook/target"
         :publishing-function org-latex-publish-to-latex
         :recursive t)
        ("latex-presentation"
         :base-directory "~/work/notebook/source"
         :base-extension "org"
         :publishing-directory "~/work/notebook/target"
         :publishing-function org-beamer-publish-to-latex
         :recursive t)
        ("latex-all" :components ("latex-article" "latex-presentation"))))

(add-to-list 'auto-mode-alist '("\\.txt$" . org-mode))

(provide 'init-org)
