$.getJSON( "orgs_with_http.json", function( jsonData ) {
  $.getJSON( "https_alternative_count.json", function( jsonData2 ) {

    var data = jsonData.map(org => {
      var el = jsonData2.find(obj => obj['org'] == org['org']);
      org['https_alt_count'] = el ? el['https_alternative_count']: null;
      return org;
    })

    $('#data-table').DataTable( {
      "autoWidth": true,
      order: [[ 1, "desc" ]],
      pagination: "bootstrap",
      filter:true,
      data: data,
      destroy: true,
      pageLength: 25,
      "columns":[  
        {"data": "org"},
        {"data": "http_count"},
        {"data": "ftp_count"},
        {"data": "https_alt_count"},
      ],
      columnDefs: [
      { "width": "8%", "targets": 4 },
      { "type": "count-percentage", "targets": 1 },
      {
        targets: 1,
        render: function (data, type, row, meta){
          if (data > 0) {
            data = data + ' (' + Math.ceil(data/row.total_count*100) +'%)';
          }
          return data;
        }
      },
      {
        targets: 2,
        render: function (data, type, row, meta){
          if (data > 0) {
            data = data + ' (' + Math.ceil(data/row.total_count*100) +'%)';
          }
          return data;
        }
      },
      {
        targets: 3,
        render: function (data, type, row, meta){
          if (data > 0) {
            data = data + ' (' + Math.ceil(data/row.total_count*100) +'%)';
          }
          return data;
        }
      },
      {
        targets: 4,
        render: function (data, type, row, meta){
          data = '<a href="org_http_resources.html?'+row.org+'">View list</a>';
          return data;
        }
      }]
    });
  });
});

//custom sort the http_count string
$.fn.dataTable.ext.type.order['count-percentage-pre'] = function ( data ) {
  if (data.indexOf(' ') != -1) {
    return parseInt(data.split(' ')[0]);
  }
  return data
};
