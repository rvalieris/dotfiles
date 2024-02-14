if [ -z "${WAYLAND_DISPLAY}" ] && [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
	systemctl --user import-environment PATH
	exec systemctl --wait --user start sway.service
fi
