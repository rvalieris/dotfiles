if [ -z "${WAYLAND_DISPLAY}" ] && [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
	source ~/.config/sway/env
	exec sway > ~/sway.log 2>&1
fi
