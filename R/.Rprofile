
options(
	"repos" = c(CRAN = "http://cran.rstudio.com/"),
	"width" = 120,
	"browser" = "firefox",
	"menu.graphics" = FALSE,
	"digits" = 15
)

if(!interactive()) {
	options(
		#warn=2,
		error=quote({
			q("no",status=1,FALSE)
		})
	)
}else{
	require(colorout)
}

