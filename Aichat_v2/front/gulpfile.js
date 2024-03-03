//引用时注意版本，版本不对会报错
var gulp = require("gulp");
var cssnano = require("gulp-cssnano");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");
var concat = require("gulp-concat");
var cache = require("gulp-cache");
var imagemin = require("gulp-imagemin");
var sass = require('gulp-sass')(require('sass'));
var bs = require("browser-sync").create();

//定义路径
var path = {
    'css':'./src/css/',
    'js':'./src/js/',
    'images':'./src/images/',
    'css_dist':'./dist/css/',
    'js_dist':'./dist/js/',
    'images_dist':'./dist/images/',
};

//定义一个css的任务,gulp4.0版本需要done回调
gulp.task("css",function (done) {
    gulp.src(path.css + '*.scss')
        .pipe(sass().on("error",sass.logError))
        .pipe(cssnano())
        .pipe(rename({"suffix":".min"}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
    done();
});

//定义一个处理js文件的任务
gulp.task("js",function (done) {
    gulp.src(path.js + '*.js')
        .pipe(uglify())
        .pipe(rename({"suffix":".min"}))
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
    done();
});

//定义一个处理图片文件的任务
gulp.task('images',function (done) {
    gulp.src(path.images + '*.*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.images_dist))
        .pipe(bs.stream())
    done()
});

let taskcss = gulp.series("css");
let taskjs = gulp.series("js");
let taskimages = gulp.series("images");
//定义监听文件修改的任务
gulp.task("watch",function (done) {
    gulp.watch(path.css + '*.scss',taskcss);
    gulp.watch(path.js + '*.js',taskjs);
    gulp.watch(path.images + '*.*',taskimages);
    done();
});

//初始化browser-sync
gulp.task("bs",function (done) {
    bs.init({
        'server':{
            'baseDir':'./'
        }
    });
    done();
});

//创建一个默认任务，4.0版本后需要在series中引用
gulp.task("default",gulp.series(['bs','watch']));

















