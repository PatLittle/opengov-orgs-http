$( document ).ready(function() {
  getDataForDatatables();
});

function getDataForDatatables(){

var url = window.location.href;
var org_id = decodeURIComponent(url.split("?").pop());
var org_name = org_id.split('|')[0].trim();
$('h1').html(org_name)

$.getJSON( "orgs_http_data.json", function( data ) {
  $.getJSON( "https_alternative_count.json", function( data2 ) {
    var el = data2.find(obj => obj['org'] == org_id);
    var https_alts = el ? el['urls'] : [];
    setDataToTable(data[org_id], https_alts);
  });
});
}

function setDataToTable(jsonData, https_alts){
$('#org-details').DataTable( {
  "autoWidth": false,
  pagination: "bootstrap",
  filter:true,
  data: jsonData,
  "scrollX": true,
  pageLength: 25,
  "columns":[  
    {"data": "dataset", width: '20%'},
    {"data": "url", width: '50%'},
    {"data": "url_type", width: '5%'},
    {"data": "dataset_id", width: '15%'},
    {"data": "id", width: '10%'},
  ],
  columnDefs: [
    {"className": "dt-center", "targets": [2,3,4,5] },
    {
      targets: 3,
      render: function (data, type, row, meta)
      {
        data = https_alts.indexOf(row.url) < 0 ? 'No': 'Yes';
        return data;
      }
    },
    {
    targets: 4,
    render: function (data, type, row, meta)
    {

      data = '<a target="_blank" href="https://open.canada.ca/data/en/dataset/' + data + '">View dataset</a>';
      return data;
    }
    },
    {
    targets: 5,
    render: function (data, type, row, meta)
    {
      if (row.from_registry) {
        return '<a target="_blank" class="btn btn-primary" href="https://registry.open.canada.ca/en/dataset/' + row.dataset_id + '/resource_edit/' + data + '">Edit resource</a>';
      }
      return 'N/A';
    }
    }
  ],
} );
}