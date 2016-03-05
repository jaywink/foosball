var gulp = require("gulp");
var production = (process.env.NODE_ENV === "production" || process.argv.indexOf("--production") > -1);


// CSS
gulp.task("css:site", require("unigulp/css")({
    name: "css:site",
    src: "foosball/static_src/less/style.less",
    dest: "foosball/static/css/foosball.css",
    production,
}));

// JS
gulp.task("js:site", require("unigulp/js")({
    name: "js:site",
    src: [
        "bower_components/jquery/dist/jquery.js",
        "bower_components/bootstrap/dist/js/bootstrap.js",
        "foosball/static_src/js/foosball.js",
    ],
    dest: "foosball/static/js/foosball.js",
    production,
}));

// FONTS
gulp.task("fonts", function () {
    return gulp.src([
        "bower_components/bootstrap/dist/fonts/*.*",
        "bower_components/font-awesome/fonts/*.*"
    ])
    .pipe(gulp.dest("foosball/static/fonts"));
});

gulp.task("watch", ["default"], function () {
    gulp.watch("foosball/static_src/less/**/*.less", ["css"]);
    gulp.watch("foosball/static_src/js/*.js", ["js"]);
});

require("unigulp/cascade")(gulp);
gulp.task("default", ["fonts", "js", "css"]);
