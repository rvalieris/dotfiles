
options(
	"repos" = c(CRAN = "https://cran.rstudio.com/"),
	"width" = tryCatch({
			as.numeric(system2("tput",c("-Txterm","cols"), stdout=T, stderr=F))
		}, error=function(e)return(120), warning=function(e)return(120)),
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
	if("colorout" %in% rownames(utils::installed.packages())) {
		require(colorout)
	}
}

sh = function(cmdline,capture=T) {
	sym = substitute(cmdline)
	if(is.symbol(sym)) { cmdline = deparse(sym) }
	.Internal(system(cmdline,capture,0))
}

