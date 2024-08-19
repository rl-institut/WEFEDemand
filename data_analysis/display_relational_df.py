# %%
from dash import Dash, ALL, dcc, html, Input, Output, State, dash_table, no_update, ctx, callback
import dash_bootstrap_components as dbc

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Initialize app
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

@callback(
    [
        Output("displayed_tables", "data", allow_duplicate=True),
        Output('app_wrapper', 'children', allow_duplicate=True),
        Output({'type': 'table', 'table_id': ALL, 'table_number': ALL}, 'data'),
    ],
    [
        Input({'type': 'table', 'table_id': ALL, 'table_number': ALL}, "active_cell"),
        Input({'type': 'close_table_button', 'table_id': ALL, 'table_number': ALL}, 'n_clicks'),
        Input({'type': 'add_row_button', 'table_id': ALL, 'table_number': ALL}, 'n_clicks'),
    ],
    [
        State({'type': 'table', 'table_id': ALL, 'table_number': ALL}, 'data'),
        State({'type': 'table', 'table_id': ALL, 'table_number': ALL}, 'columns'),
        State('displayed_tables', 'data'),
        State('app_wrapper', 'children')
    ],
    prevent_initial_call=True

)
def update_tables(active_cell,
                  close_table_button_clicks,
                  add_row_button_clicks,
                  displayed_tables_data,
                  displayed_tables_columns,
                  displayed_tables_list,
                  current_tables_view):
    """
    Callback function to run when a cell of a table is clicked

    :param active_cell:
    :param close_table_button_clicks:
    :param add_row_button_clicks:
    :param displayed_tables_list:
    :param current_tables_view:
    :return:
    """
    print(active_cell)
    # Get id of table that was clicked: ID is dict with the following entries:
    # "type": "table", -> fix identifier for every table
    # "table_id": relational_df.table_id,  -> specific ID of this table
    # "table_number": table_number  -> number of the table in the list of displayed tables

    # Get ID of element that was clicked -> decide which action to perform
    element_clicked = ctx.triggered_id

    if element_clicked['type'] == 'table':
        # Run table cell clicked actions
        logging.debug('Table cell clicked')
        # Abort if there is no active cell or no table clicked
        if active_cell[0] is None:
            return no_update

        test = table_cell_clicked(active_cell, displayed_tables_list, current_tables_view) + (displayed_tables_data,)

        return table_cell_clicked(active_cell, displayed_tables_list, current_tables_view) + (displayed_tables_data,)

    elif element_clicked['type'] == 'close_table_button':
        # Run close table button clicked actions
        logging.debug('Close table button clicked')
        return (close_table_button_clicked(close_table_button_clicks, displayed_tables_list, current_tables_view)
                + (displayed_tables_data,))
    elif element_clicked['type'] == 'add_row_button':
        logging.debug('Add row button clicked')
        return add_table_row(add_row_button_clicks, displayed_tables_data, displayed_tables_columns,
                             displayed_tables_list, current_tables_view)


def table_cell_clicked(active_cell, displayed_tables, current_tables_view):
    table_clicked = ctx.triggered_id

    # Check if the clicked column is child column and contains sub-data
    if active_cell[table_clicked['table_number']]['column_id'].startswith('!child_'):
        # Reset active cell to invisible cell

        # Get child_table_id from the clicked column
        child_table_id = active_cell[table_clicked['table_number']]['column_id'][7:]

        # Get the corresponding query_col of the child table
        query_col = display_tables_dict[table_clicked['table_id']].child_tables[child_table_id].parent_tables[
            table_clicked['table_id']][1]
        # Get corresponding query_id
        query_id = active_cell[table_clicked['table_number']]['row_id']

        # Check if this table is already displayed
        if child_table_id not in displayed_tables:
            logging.debug('Add new table')

            # Generate new table to display
            new_table = display_table(
                relational_df=display_tables_dict[table_clicked['table_id']].child_tables[child_table_id],
                table_number=len(current_tables_view),  # position of new table is at the end of current tables view
                query_col=query_col,
                query_id=query_id
            )

            # Add new table to App view
            current_tables_view.append(new_table)

            # Add to dict of displayed tables (query_col, query_id)
            displayed_tables[child_table_id] = (query_col, query_id)

        else:
            logging.debug('Table is already displayed')
            # Check if already displayed table has the same query_id
            if displayed_tables.get(child_table_id)[1] == active_cell[table_clicked['table_number']]['row_id']:
                logging.debug('Same query ID')  # Do nothing
            else:
                logging.debug('New query ID')
                # Close the displayed table and all tables below
                # Get position of first table to close
                position = list(displayed_tables).index(child_table_id)

                # Remove table and all following from the dict of displayed tables
                displayed_tables = dict(list(displayed_tables.items())[0:position])

                # Remove table and all following tables from the tables view
                current_tables_view = current_tables_view[0:position]

                # Add new table with new query_id
                new_table = display_table(
                    relational_df=display_tables_dict[table_clicked['table_id']].child_tables[child_table_id],
                    table_number=len(current_tables_view),  # position of new table is at the end of current tables view
                    query_col=query_col,
                    query_id=query_id
                )

                # Add new table to App view
                current_tables_view.append(new_table)

                # Add to dict of displayed tables (query_col, query_id)
                displayed_tables[child_table_id] = (query_col, query_id)

    # Return dict of displayed tables and updated view (HTML) if currently displayed tables and None for active cell
    return displayed_tables, current_tables_view


def close_table_button_clicked(n, displayed_tables, current_tables_view):
    logging.debug('Button clicked:')
    logging.debug(ctx.triggered_id)

    button_clicked = ctx.triggered_id
    # Remove this close button's corresponding table and all following from the dict of displayed tables
    displayed_tables = dict(list(displayed_tables.items())[0:button_clicked['table_number']])

    # Remove this close button's corresponding table and all following tables from the tables view
    current_tables_view = current_tables_view[0:button_clicked['table_number']]

    return displayed_tables, current_tables_view


def add_table_row(n, displayed_tables_data, displayed_tables_columns, displayed_tables, current_tables_view):
    logging.debug('Add table row button clicked:')
    logging.debug(ctx.triggered_id)
    button_clicked = ctx.triggered_id

    # Get columns of table to which row is added
    columns = displayed_tables_columns[button_clicked['table_number']]
    # Construct new row entry
    new_row = {}
    for col in columns:
        if col['id'].startswith('!child_'):  # for button column
            new_row[col['id']] = 'Click me! (added)'
        elif col['id'] == 'id':  # for element id column
            # Generate ID of new element to add -> must be unique! -> current max id +1
            #TODO
            new_row[col['id']] = display_tables_dict[button_clicked['table_id']].df['id'].max() + 1
        elif col['id'] == displayed_tables[button_clicked['table_id']][0]:  # for query_col
            # Enter query_id
            new_row[col['id']] = displayed_tables[button_clicked['table_id']][1]  # value is query_id
        else:
            new_row[col['id']] = ""

    displayed_tables_data[button_clicked['table_number']].append(new_row)

    return displayed_tables, current_tables_view, displayed_tables_data


def display_table(relational_df, table_number, query_col=None, query_id=None):
    """
    Generates and returns new "row" containing Dash data table to add to the layout

    :param relational_df: containing data to display in this table
    :param table_number: position, at which this table will be displayed
    :param query_col: foreign_key column to query the dataframe for, default=None
    :param query_id: ID to query parent table for (ID of the entry in the clicked row)
    :return:
    """

    # Check if query data is provided
    if query_col and query_id:
        # If specified, query table for foreign key
        df = relational_df.df.query(str(query_col) + ' == ' + str(query_id))
    else:
        # Otherwise create copy of the dataframe to display
        df = relational_df.df.copy()

    # Get this relational_df's foreign key columns -> to not display them
    foreign_key_columns = []
    for parent_table in relational_df.parent_tables.values():
        foreign_key_columns.append(parent_table[1])

    # Get this tables original columns
    original_columns = []
    for c in df.columns:
        if c == 'id':  # If column is ID column...
            original_columns.append(
                {"name": c, "id": c, "editable": False}  # ...it is NOT editable
            )
        elif c in foreign_key_columns:  # If column is foreign_key column
            original_columns.append(
                {"name": c, "id": c, "editable": False}  # ...it is NOT editable
            )
        else:  # Every regular column...
            original_columns.append(
                {"name": c, "id": c, "editable": True}  # ...is editable
            )

    # Create new "button" column for this table -> to link to child tables
    child_table_columns = []

    # Create button column for every child table of this dataframe
    for child_table_id, child_table_relational_df in relational_df.child_tables.items():
        child_table_columns.append(
            {'name': child_table_relational_df.table_name,  # Column name is child_table name
             'id': "!child_"+str(child_table_id),
             'editable': False  # "Button column" is not editable
             }
        )  # Column ID is identifier + child_table id
        # Add "button text" to display in the button column
        if len(df.index) > 0:  # only if the table to display is not empty
            df.loc[:, "!child_"+str(child_table_id)] = 'Click me!'

    # Add original and custom created child_table columns
    columns = original_columns + child_table_columns

    # Generate dash datatable object
    table = dash_table.DataTable(
        id={"type": "table", "table_id": relational_df.table_id, "table_number": table_number},
        columns=columns,
        data=df.to_dict("records"),
        page_size=10,
        sort_action="native",
        active_cell=None,
        editable=True,
        filter_action="native",
        sort_mode='multi',
        row_selectable='multi',
        row_deletable=True,
        selected_rows=[],
        page_action='native',
        page_current=0,
    ),

    # Create new row to add to app HTML layout

    # Generate header for new table
    if query_col:  # If table is queried, add query column name in header
        header = query_col + ': ' + str(query_id) + ' - ' + relational_df.table_name
    else:
        header = relational_df.table_name

    new_table_row = html.Div(
        [
            dbc.Row(dbc.Col(html.H2(header))),
            dbc.Row(
                [
                    dbc.Col(table, width=11),
                    dbc.Col(
                        [
                            dbc.Button('X', id={
                                'type': 'close_table_button',
                                "table_id": relational_df.table_id,
                                "table_number": table_number
                            }) if table_number !=0 else None,  # don't display close button for first table
                            dbc.Button('Add row', id={
                                'type': 'add_row_button',
                                "table_id": relational_df.table_id,
                                'table_number': table_number
                            }),
                        ],
                        width=1)
                ])

        ], id=relational_df.table_id, className='table_row_wrapper'
    )

    return new_table_row


from data_analysis.data_analysis_test import display_tables_dict  # dict containing all tables to be displayed
from data_analysis.data_analysis_test import first_table  # first table to be displayed

# Initialize layout (with users table)
app.layout = html.Div(
    [
        # Save ID of first displayed table for position
        # dict: {table_id: ('query_column', 'query_id')}
        dcc.Store(id='displayed_tables', data={first_table.table_id: (None, None)}),
        # Add first displayed table to app_wrapper
        html.Div([display_table(first_table, 0)], id='app_wrapper')
    ]
)

if __name__ == '__main__':
    app.run_server(debug=False, port=8051)
    logging.debug('App running')
