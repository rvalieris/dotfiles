
options(
	"repos" = c(CRAN = "https://cran.rstudio.com/"),
	"width" = 120,
	"browser" = "firefox",
	"menu.graphics" = FALSE,
	"digits" = 15
)

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

