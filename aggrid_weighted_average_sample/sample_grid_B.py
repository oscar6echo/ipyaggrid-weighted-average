import os
import json


from dotenv import load_dotenv
from ipyaggrid import Grid

from copy import deepcopy as copy
from IPython.display import display, HTML
from timeit import default_timer as timer


plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)


def build_grid_B(df):
    """
    """

    helpers_custom = r"""
    helpersCustom = {
        formatFloat1: d3.format(',.1f'),
        formatFloat2: d3.format(',.2f'),
        formatFloat3: d3.format(',.3f'),
    }
    """

    js_post_grid = [
        r"""
    window.go = gridOptions;
    var arrData = [];
    gridOptions.api.forEachNodeAfterFilterAndSort(node=>{
        //console.log(node.data);
        arrData.push(node.data);
    })
    console.log('arrData')
    console.log(arrData)

    arrData = arrData.filter(e => (e!= undefined));
    console.log('arrData')
    console.log(arrData)
    gridOptions.context = {
        max_volume: Math.max(...arrData.map(e => e.volume)),
        min_volume: Math.min(...arrData.map(e => e.volume)),
    };
    console.log('gridOptions.context')
    console.log(gridOptions.context)
    """,
    ]

    # format_int = 'function(params){ return helpers.formatInt(params.value); }'
    format_float2 = r'function(params){ return helpers.formatFloat2(params.value); }'
    # format_float3 = r'function(params){ return helpers.formatFloat3(params.value); }'

    cell_renderer_volume = r"""
    function(params) {
        let v = params.value;
        let min_ = params.context.min_volume;
        let max_ = params.context.max_volume;
        var f = Math.round(100 * v / max_, 2);
        let color = '#bcbddc';
        let css = `background: linear-gradient(to right, ${color} ${f}%, transparent ${f}%, transparent 100%)`;
        let html = `<div style=\"${css}\">${helpers.formatFloat1(v)}</div>`;
        return html;
    }
    """

    columnDefs = [
        {
            'headerName': 'Client',
            'field': 'client',
            'width': 150,
            'rowGroup': True,
            'hide': True,

        },
        {
            'headerName': 'Level',
            'field': 'level',
            'width': 150,
            'valueFormatter': format_float2,
        },
        {
            'headerName': 'Volume',
            'field': 'volume',
            'width': 150,
            'cellRenderer': cell_renderer_volume,
        },
        {
            'headerName': 'Price',
            'field': 'price',
            'width': 150,
        },
    ]

    css_rules = """
    .ag-row-level-1 {
        background-color: #fee6ce !important;
    }
    """

    groupRowAggNodesB = r"""
function groupRowAggNodes(nodes) {
  console.log(nodes);

  const buildWeightAverage = function(colName, refColName) {
    let sumCol = 0;
    let sumRef = 0;
    let sumProduct = 0;
    nodes.forEach(node => {
      const data = node.group ? node.aggData : node.data;
      sumRef += data[refColName];
      sumProduct += (data[colName] * data[refColName]);
    });
    return sumProduct / sumRef;
  };

  const buildSum = function(colName) {
    let sumCol = 0;
    nodes.forEach(node => {
      const data = node.group ? node.aggData : node.data;
      sumCol += data[colName];
    });
    return sumCol;
  };

  const refCol = "volume";
  const colsToWeightAverage = ["level"];

  const colsToSum = ["price"];

  const resultSum = colsToSum.reduce((acc, cur) => {
    acc[cur] = buildSum(cur);
    return acc;
  }, {});

  const resultWeightAverage = colsToWeightAverage.reduce((acc, cur) => {
    acc[cur] = buildWeightAverage(cur, refCol);
    return acc;
  }, {});

  const result = {
    ...{ [refCol]: buildSum(refCol) },
    ...resultSum,
    ...resultWeightAverage
  };

  console.log(result);
  return result;
}

    """

    gridOptions = {
        'pivotMode': False,
        'enableFilter': True,
        'enableSorting': True,
        'enableColResize': True,
        'columnDefs': columnDefs,
        'groupHideOpenParents': False,
        'suppressAggFuncInHeader': True,
        'groupRowAggNodes': groupRowAggNodesB,
    }

    grid = Grid(
        width=700,
        height=700,
        quick_filter=True,
        theme='ag-theme-balham',
        compress_data=True,
        grid_options=gridOptions,
        grid_data=df,
        js_helpers_custom=helpers_custom,
        js_post_grid=js_post_grid,
        css_rules=css_rules,
        columns_fit='',
        license='',
    )

    html = grid.export_html(build=True)
    path = os.path.join(plot_folder, 'plot_grid_B.html')
    with open(path, 'w') as f:
        f.write(html)

    path0 = path

    print('grid saved to {}'.format(path))

    html_export = grid.export_html()

    path = os.path.join(plot_folder, 'widget_div_B.html')
    with open(path, 'w') as f:
        f.write(html_export['grid_div'])
    print('\tsaved widget div to {}'.format(path))

    path = os.path.join(plot_folder, 'widget_state_B.json')
    with open(path, 'w') as f:
        f.write(json.dumps(html_export['manager_state']))
    print('\tsaved widget state to {}'.format(path))

    cwd = os.getcwd()
    path = os.path.join(cwd, path0)

    print(f'open file:\n{path}')
