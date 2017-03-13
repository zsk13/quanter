$(function() {

    $('#tablepool').bootstrapTable({
        striped: true,
        sidePagination: "client",
        pageNumber: 1,
        pageSize: 10,
        pageList: [10, 25, 50, 100],
        height: 400,
        clickToSelect: true,
        columns: [{
            field: 'id',
            title: '股票代码'
        }, {
            field: 'name',
            title: '股票名称'
        }],
        data: stocks
        // data: [{
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行'
        // }]
    });
    $('#table').bootstrapTable({
        striped: true,
        sidePagination: "client",
        pageNumber: 1,
        height: 187,
        clickToSelect: true,
        columns: [{
            checkbox: true
        }, {
            field: 'id',
            title: '股票代码'
        }, {
            field: 'name',
            title: '股票名称'
        }, {
            field: 'recommend',
            title: '推荐等级'
        }],
        data:recommends
        // data: [{
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }, {
        //     id: 'sh601998',
        //     name: '中国银行',
        //     recommend: '5'
        // }]
    })
});
$('#tablebuy').bootstrapTable({
    striped: true,
    sidePagination: "client",
    pageNumber: 1,
    height: 200,
    clickToSelect: true,
    columns: [{
        field: 'id',
        title: '股票代码'
    }, {
        field: 'name',
        title: '股票名称'
    }, {
        field: 'buyprice',
        title: '买入条件'
    }],
    data: [{
        id: 'sh601998',
        name: '中国银行',
        buyprice: '5.1'
    }, {
        id: 'sh601998',
        name: '中国银行',
        buyprice: '5.1'
    }, {
        id: 'sh601998',
        name: '中国银行',
        buyprice: '5.1'
    }, {
        id: 'sh601998',
        name: '中国银行',
        buyprice: '5.1'
    }, {
        id: 'sh601998',
        name: '中国银行',
        buyprice: '5.1'
    }]
});
$('#tablesale').bootstrapTable({
    striped: true,
    sidePagination: "client",
    pageNumber: 1,
    height: 200,
    clickToSelect: true,
    columns: [{
        field: 'id',
        title: '股票代码'
    }, {
        field: 'name',
        title: '股票名称'
    }, {
        field: 'saleprice',
        title: '卖出条件'
    }],
    data: [{
        id: 'sh601998',
        name: '中国银行',
        saleprice: '5.2'
    }, {
        id: 'sh601998',
        name: '中国银行',
        saleprice: '5.2'
    }, {
        id: 'sh601998',
        name: '中国银行',
        saleprice: '5.2'
    }, {
        id: 'sh601998',
        name: '中国银行',
        saleprice: '5.2'
    }, {
        id: 'sh601998',
        name: '中国银行',
        saleprice: '5.2'
    }]
});