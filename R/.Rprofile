
options(
	"repos" = c(CRAN = "https://cran.rstudio.com/"),
	"width" = 120,
	"browser" = "firefox",
	"menu.graphics" = FALSE,
	"digits" = 15
)

# autocomplete library/require
utils::rc.settings(ipck=TRUE)

if(!interactive()) {
	options(
		warn=1,
		error=quote({
			q("no",status=1,FALSE)
		})
	)
}else{
	require(colorout)
}

shell = function(cmdline,capture=F) {
	sym = substitute(cmdline)
	if(!is.symbol(sym)) { stop("use backticks") }
	.Internal(system(deparse(sym),capture,0))
}

