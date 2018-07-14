let gulp         = require("gulp"),
    babel        = require("gulp-babel"),
    del          = require("del"),
    uglify       = require("gulp-uglify"),
    sourcemaps   = require('gulp-sourcemaps')


// Watch asset folder for changes
gulp.task("watch", ["js"], () => {
    gulp.watch("js/**/*", ["js"])
})

gulp.task("js", () => {
    gulp.src([
        "js/**/*",
    ])
    .pipe(sourcemaps.init())
    .pipe(babel({
        "presets": [["@babel/env", {
            "targets": {
                // The % refers to the global coverage of users from browserslist
                "browsers": [ ">0.25%", "not op_mini all"]
            }
        }]],
    }))
    .pipe(uglify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest("dist/"))
    .pipe(gulp.dest("wsync/static/"))
})

gulp.task("build", ["js"])
gulp.task("default", ["watch"])
