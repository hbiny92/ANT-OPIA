const express = require('express');
const router = express.Router();
const admin = require('firebase-admin');
const serviceAccount = require('../media-fin-firebase-adminsdk-8oysm-ea8cc82bdf.json');


const firebaesAdmin = admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: 'https://media-fin.firebaseio.com'
});
const database = firebaesAdmin.database()

//프론트로보낼
var ent_data1, ent_data2, ent_data3, ent_data4, ent_data5, news_data1, news_data2, news_data3, news_data4
    , news_data5, news_data6, news_data7, news_data8, news_data9, news_data10,index, re_data1,re_data2
    ,re_data3,re_data4,re_data5,re_data6


router.get('/', function (req, res, next) {

    // 국내 주가데이터
    var spawn = require('child_process').spawn;
    var process = spawn('python', ["./public/python/crawling_index.py"]);
    process.stdout.on('data', (data1) => {
        var index = data1.toString();
        var data = index.split("'");
        var userdata = {
            "KOSPI": data[1], "KOSPI변화": data[3],"KOSPI변화상태":data[5],
            "KOSDAQ": data[7], "KOSDAQ변화": data[9],"KOSDAQ변화상태":data[11],
            "KOSPI200": data[13], "KOSPI200변화": data[15],"KOSPI200변화상태":data[17],
        };
        database.ref('실시간주가').update(userdata);
    });

    //환율데이터
    var spawn = require('child_process').spawn;
    var process6 = spawn('python', ["./public/python/crawling_currency.py"]);
    process6.stdout.on('data', (data1) => {
        var index = data1.toString();
        var data = index.split("'");
        var userdata = {
            "달러환율":data[1],"달러환율변동":data[3],"달러환율변동상태":data[5],
            "엔화환율":data[7],"엔화환율변동":data[9],"엔화환율변동상태":data[11],
            "유로환율":data[13],"유로환율변동":data[15],"유로환율변동상태":data[17]
        };
        database.ref('실시간주가').update(userdata);
    });

    //주가, 환율 db값 가져오기
    var ref_currency = database.ref('실시간주가')
    ref_currency.on('value', function (snapshot) {
        index = snapshot.val()
    });


    //기업데이터1
    var process3 = spawn('python', ["./public/python/crawling_enterprise_data_2.py"]);
    process3.stdout.on('data', (data3) => {
        var index = data3.toString();
        var data = index.split("'");
        var userdata = {
            "현재가": data[1], "시가": data[3], "전일대비": data[5], "등락률": data[7], "거래량": data[9]
            , "시가총액": data[11], "고가": data[13], "저가": data[15], "PER": data[17], "EPS": data[19]
        };
        for (var i = 0; i < userdata.length; i++) {
            ent_data[i] = userdata[i]
        }
        database.ref('samsung_electronics/기업데이터').update(userdata);
    });

    //db값 가져오기
    var ref_entdata1 = database.ref('/samsung_electronics/기업데이터');

    ref_entdata1.on('value', function (snapshot) {
        ent_data1 = snapshot.val()
    });


    //기업데이터2
    //분기실적데이터 18.09 18.12 19.03 19.06 순서대로 가져온다
    var process2 = spawn('python', ["./public/python/crawling_enterprise_data.py"]);
    process2.stdout.on('data', (data2) => {
        var index2 = data2.toString()
        var data = index2.split("'");
        //순서대로 18년3분기 4분기 19년 1분기 2분기
        var userdata1 = {
            "매출액": data[9], "영업이익": data[11], "당기순이익": data[13], "영업이익률": data[15]
        };
        var userdata2 = {
            "매출액": data[17], "영업이익": data[19], "당기순이익": data[21], "영업이익률": data[23]
        };
        var userdata3 = {
            "매출액": data[25], "영업이익": data[27], "당기순이익": data[29], "영업이익률": data[31]
        };
        var userdata4 = {
            "매출액": data[33], "영업이익": data[35], "당기순이익": data[37], "영업이익률": data[39]
        };
        database.ref('samsung_electronics/기업분기실적/18년3분기').update(userdata1);
        database.ref('samsung_electronics/기업분기실적/18년4분기').update(userdata2);
        database.ref('samsung_electronics/기업분기실적/19년1분기').update(userdata3);
        database.ref('samsung_electronics/기업분기실적/19년2분기').update(userdata4);

    });

    //분기실적 데이터 db값 가져오기
    var ref_entdata2 = database.ref('/samsung_electronics/기업분기실적/18년3분기');
    var ref_entdata3 = database.ref('/samsung_electronics/기업분기실적/18년4분기');
    var ref_entdata4 = database.ref('/samsung_electronics/기업분기실적/19년1분기');
    var ref_entdata5 = database.ref('/samsung_electronics/기업분기실적/19년2분기');

    ref_entdata2.on('value', function (snapshot) {
        ent_data2 = snapshot.val()
    });
    ref_entdata3.on('value', function (snapshot) {
        ent_data3 = snapshot.val()
    });
    ref_entdata4.on('value', function (snapshot) {
        ent_data4 = snapshot.val()
    });
    ref_entdata5.on('value', function (snapshot) {
        ent_data5 = snapshot.val()
    });


    //뉴스데이터
    var process4 = spawn('python', ["./public/python/crawling_news2.py"]);
    process4.stdout.on('data', (data5) => {
        var index = data5.toString();
        var data = index.split("'");

        var userdata1 = {
            "제목": data[1], "시간": data[21], "출처": data[41], "내용": data[61], "링크": data[81]
        };
        var userdata2 = {
            "제목": data[3], "시간": data[23], "출처": data[43], "내용": data[63], "링크": data[83]
        };
        var userdata3 = {
            "제목": data[5], "시간": data[25], "출처": data[45], "내용": data[65], "링크": data[85]
        };
        var userdata4 = {
            "제목": data[7], "시간": data[27], "출처": data[47], "내용": data[67], "링크": data[87]
        };
        var userdata5 = {
            "제목": data[9], "시간": data[29], "출처": data[49], "내용": data[69], "링크": data[89]
        };
        var userdata6 = {
            "제목": data[11], "시간": data[31], "출처": data[51], "내용": data[71], "링크": data[91]
        };
        var userdata7 = {
            "제목": data[13], "시간": data[33], "출처": data[53], "내용": data[73], "링크": data[93]
        };
        var userdata8 = {
            "제목": data[15], "시간": data[35], "출처": data[55], "내용": data[75], "링크": data[95]
        };
        var userdata9 = {
            "제목": data[17], "시간": data[37], "출처": data[57], "내용": data[77], "링크": data[97]
        };
        var userdata10 = {
            "제목": data[19], "시간": data[39], "출처": data[59], "내용": data[79], "링크": data[99]
        };

        database.ref('samsung_electronics/뉴스/1번뉴스').update(userdata1);
        database.ref('samsung_electronics/뉴스/2번뉴스').update(userdata2);
        database.ref('samsung_electronics/뉴스/3번뉴스').update(userdata3);
        database.ref('samsung_electronics/뉴스/4번뉴스').update(userdata4);
        database.ref('samsung_electronics/뉴스/5번뉴스').update(userdata5);
        database.ref('samsung_electronics/뉴스/6번뉴스').update(userdata6);
        database.ref('samsung_electronics/뉴스/7번뉴스').update(userdata7);
        database.ref('samsung_electronics/뉴스/8번뉴스').update(userdata8);
        database.ref('samsung_electronics/뉴스/9번뉴스').update(userdata9);
        database.ref('samsung_electronics/뉴스/10번뉴스').update(userdata10);
    });

    //뉴스데이터 db서 가져오기
    var ref_newdata1 = database.ref('/samsung_electronics/뉴스/1번뉴스');
    var ref_newdata2 = database.ref('/samsung_electronics/뉴스/2번뉴스');
    var ref_newdata3 = database.ref('/samsung_electronics/뉴스/3번뉴스');
    var ref_newdata4 = database.ref('/samsung_electronics/뉴스/4번뉴스');
    var ref_newdata5 = database.ref('/samsung_electronics/뉴스/5번뉴스');
    var ref_newdata6 = database.ref('/samsung_electronics/뉴스/6번뉴스');
    var ref_newdata7 = database.ref('/samsung_electronics/뉴스/7번뉴스');
    var ref_newdata8 = database.ref('/samsung_electronics/뉴스/8번뉴스');
    var ref_newdata9 = database.ref('/samsung_electronics/뉴스/9번뉴스');
    var ref_newdata10 = database.ref('/samsung_electronics/뉴스/10번뉴스');

    ref_newdata1.on('value', function (snapshot) {
        news_data1 = snapshot.val()
    });
    ref_newdata1.on('value', function (snapshot) {
        news_data1 = snapshot.val()
    });
    ref_newdata2.on('value', function (snapshot) {
        news_data2 = snapshot.val()
    });
    ref_newdata3.on('value', function (snapshot) {
        news_data3 = snapshot.val()
    });
    ref_newdata4.on('value', function (snapshot) {
        news_data4 = snapshot.val()
    });
    ref_newdata5.on('value', function (snapshot) {
        news_data5 = snapshot.val()
    });
    ref_newdata6.on('value', function (snapshot) {
        news_data6 = snapshot.val()
    });
    ref_newdata7.on('value', function (snapshot) {
        news_data7 = snapshot.val()
    });
    ref_newdata8.on('value', function (snapshot) {
        news_data8 = snapshot.val()
    });
    ref_newdata9.on('value', function (snapshot) {
        news_data9 = snapshot.val()
    });
    ref_newdata10.on('value', function (snapshot) {
        news_data10 = snapshot.val()
    });

    //연관기업데이터
    var ref_relative1 = database.ref('/samsung_electronics/연관기업/1');
    ref_relative1.on('value', function (snapshot) {
        re_data1 = snapshot.val()
    });
    var ref_relative2 = database.ref('/samsung_electronics/연관기업/2');
    ref_relative2.on('value', function (snapshot) {
        re_data2 = snapshot.val()
    });
    var ref_relative3 = database.ref('/samsung_electronics/연관기업/3');
    ref_relative3.on('value', function (snapshot) {
        re_data3 = snapshot.val()
    });
    var ref_relative4 = database.ref('/samsung_electronics/연관기업/4');
    ref_relative4.on('value', function (snapshot) {
        re_data4 = snapshot.val()
    });
    var ref_relative5 = database.ref('/samsung_electronics/연관기업/5');
    ref_relative5.on('value', function (snapshot) {
        re_data5 = snapshot.val()
    });
    var ref_relative6 = database.ref('/samsung_electronics/연관기업/6');
    ref_relative6.on('value', function (snapshot) {
        re_data6 = snapshot.val()
    });

    res.render('layout', {
        //실시간 지수 , 환율
        Index:index,

        //기업데이터, 실적데이터
        Ent_data1: ent_data1, Ent_data2: ent_data2, Ent_data3: ent_data3
        , Ent_data4: ent_data4, Ent_data5: ent_data5,

        //뉴스데이터
        News_data1: news_data1, News_data2: news_data2, News_data3: news_data3, News_data4: news_data4,
        News_data5: news_data5, News_data6: news_data6, News_data7: news_data7, News_data8: news_data8,
        News_data9: news_data9, News_data10: news_data10,

        //연관기업데이터
        Re_data1:re_data1,Re_data2:re_data2,Re_data3:re_data3,Re_data4:re_data4,Re_data5:re_data5,Re_data6:re_data6
    });

});

module.exports = router;

