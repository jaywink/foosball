var gulp = require("gulp");
var production = (process.env.NODE_ENV === "production" || process.argv.indexOf("--production") > -1);


// CSS
gulp.task("css:site", require("unigulp/css")({
    name: "css:site",
    src: "foosball/static_src/less/style.less",
    dest: "foosball/static/css/foosball.css",
    production
}));

// JS
gulp.task("js:site", require("unigulp/js")({
    name: "js:site",
    src: [
        "bower_components/jquery/dist/jquery.js",
        "bower_components/bootstrap/dist/js/bootstrap.js",
        "bower_components/Chart.js/dist/Chart.min.js",
        "foosball/games/static_src/js/stats.js"
    ],
    dest: "foosball/static/js/foosball.js",
    production
}));

// FONTS
gulp.task("fonts:general", function () {
    return gulp.src([
        "bower_components/bootstrap/dist/fonts/*.*",
        "bower_components/font-awesome/fonts/*.*"
    ])
    .pipe(gulp.dest("foosball/static/fonts"));
});

gulp.task("fonts:lobster", function () {
    return gulp.src("bower_components/fontkit-lobster/fonts/lobster/*.*")
        .pipe(gulp.dest("foosball/static/fonts/lobster"));
});

gulp.task("css:lobster", function () {
    return gulp.src("bower_components/fontkit-lobster/styles/lobster.css")
        .pipe(gulp.dest("foosball/static/css"));
});


gulp.task("watch", ["default"], function () {
    gulp.watch("foosball/static_src/less/**/*.less", ["css"]);
    gulp.watch("foosball/static_src/js/*.js", ["js"]);
});

require("unigulp/cascade")(gulp);
gulp.task("default", ["fonts", "js", "css"]);
