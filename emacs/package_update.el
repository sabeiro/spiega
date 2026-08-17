(defcustom package-last-refresh-date nil
  "Date and time when package lists have been refreshed.")

(defcustom package-automatic-refresh-threshold 24
  "Amount of hours since last `package-refresh-contents' call needed to trigger automatic refresh before calling `package-install'.")

(package-refresh-contents)
(package-update-all)
(list-packages)
(package-install magit)
;setq transient--set-layout)
(use-package transient)
(use-package magit)


(use-package auto-package-update
   :ensure t
   :config
   (setq auto-package-update-delete-old-versions t
         auto-package-update-interval 4)
   (auto-package-update-maybe))

(use-package paradox
  :init
  (setq paradox-github-token t)
  (setq paradox-execute-asynchronously t)
  (setq paradox-automatically-star t))
