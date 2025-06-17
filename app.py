import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
from statistical_test import Statistical_test

# Load dataset
df = pd.read_csv("country_wise_latest.csv")
st = Statistical_test()

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "COVID Statistical Test Dashboard"

# ✅ Updated form_group with conditional ID
def form_group(label, component, id_suffix=None):
    kwargs = {'className': 'form-group'}
    if id_suffix is not None:
        kwargs['id'] = id_suffix
    return html.Div([
        html.Label(label, className="form-label"),
        component
    ], **kwargs)

# Prepare dropdown options
condition_options = [
    {'label': '>', 'value': '>'},
    {'label': '<', 'value': '<'},
    {'label': '>=', 'value': '>='},
    {'label': '<=', 'value': '<='},
    {'label': '==', 'value': '=='}
]
region_options = [{'label': r, 'value': r} for r in sorted(df['WHO Region'].dropna().unique())]

app.layout = html.Div([
    html.Div([
        html.H2("COVID-19 Statistical Tests", className="app-title"),

        form_group("Select Test Type", dcc.Dropdown(id='test-type', options=[
            {'label': 'Chi-Square Test (Binary vs Group)', 'value': 'chi-square'},
            {'label': 'Two Sample T-Test', 'value': 'two-ttest'},
            {'label': 'One Sample T-Test', 'value': 'one-ttest'},
            {'label': 'Z-Test for Proportions', 'value': 'ztest'}
        ], value='chi-square', className="dropdown")),

        html.Hr(),

        html.Div(id='dynamic-inputs', children=[
            form_group("Group Column", dcc.Dropdown(
                id='group-col',
                options=[{'label': c, 'value': c} for c in df.select_dtypes(include='object').columns],
                value='WHO Region',
                className="dropdown"
            ), id_suffix='group-col-container'),

            form_group("Numeric Column", dcc.Dropdown(
                id='numeric-col',
                options=[{'label': c, 'value': c} for c in df.select_dtypes(include='number').columns],
                value='Recovered / 100 Cases',
                className="dropdown"
            ), id_suffix='numeric-col-container'),

            form_group("Condition (>, <, >=, <=, ==)", dcc.Dropdown(
                id='condition',
                options=condition_options,
                value='>',
                className="dropdown"
            ), id_suffix='condition-container'),

            form_group("Threshold Value", dcc.Input(
                id='threshold',
                type='number',
                value=70
            ), id_suffix='threshold-container'),

            form_group("Region 1", dcc.Dropdown(
                id='region1',
                options=region_options,
                value='Europe',
                className="dropdown"
            ), id_suffix='region1-container'),

            form_group("Region 2", dcc.Dropdown(
                id='region2',
                options=region_options,
                value='Africa',
                className="dropdown"
            ), id_suffix='region2-container'),

            form_group("Tail Type (greater, less, two-sided)", dcc.Input(
                id='tail',
                type='text',
                value='greater'
            ), id_suffix='tail-container')
        ]),

        html.Div([
            html.Button("Run Test", id='run-test', n_clicks=0, className="button")
        ], style={"marginTop": "20px"}),

        html.Hr(),
        html.Div(id='test-output', className="result-box")

    ], className="container")
])

# Show/hide fields based on selected test
@app.callback(
    Output('group-col-container', 'style'),
    Output('numeric-col-container', 'style'),
    Output('condition-container', 'style'),
    Output('threshold-container', 'style'),
    Output('region1-container', 'style'),
    Output('region2-container', 'style'),
    Output('tail-container', 'style'),
    Input('test-type', 'value')
)
def update_visibility(test_type):
    hide = {'display': 'none'}
    show = {'display': 'block'}
    return (
        show if test_type in ['chi-square', 'ztest'] else hide,
        show if test_type in ['chi-square', 'ztest', 'one-ttest', 'two-ttest'] else hide,
        show if test_type in ['chi-square', 'ztest'] else hide,
        show if test_type in ['chi-square', 'ztest'] else hide,
        show if test_type in ['ztest', 'two-ttest', 'one-ttest'] else hide,
        show if test_type in ['ztest', 'two-ttest'] else hide,
        show if test_type == 'one-ttest' else hide
    )

# Main test execution logic
@app.callback(
    Output('test-output', 'children'),
    Input('run-test', 'n_clicks'),
    State('test-type', 'value'),
    State('group-col', 'value'),
    State('numeric-col', 'value'),
    State('condition', 'value'),
    State('threshold', 'value'),
    State('region1', 'value'),
    State('region2', 'value'),
    State('tail', 'value')
)
def run_test(n, test_type, group_col, num_col, cond, threshold, region1, region2, tail):
    if n == 0:
        return "Waiting for input..."

    try:
        if test_type == 'chi-square':
            t, p, dof, _ = st.chi_square_test_binary(df, group_col, num_col, cond, threshold)
        elif test_type == 'two-ttest':
            t, p = st.two_sample_ttest(df, region1, region2)
        elif test_type == 'one-ttest':
            t, p = st.one_sample_ttest(df, num_col, region1, tail)
        elif test_type == 'ztest':
            t, p = st.z_test_proportions(df, region1, region2, threshold, num_col, sign=tail)
        else:
            return "Invalid test type selected."

        if t is None or p is None:
            return "❌ Test failed due to missing or invalid data."

        return html.Div([
            html.H4("✅ Test Results:"),
            html.P(f"Test Statistic: {t:.4f}"),
            html.P(f"P-Value: {p:.4f}"),
            html.P(f"Conclusion: {st.hypothesis_test()}")
        ])

    except Exception as e:
        return html.Div([
            html.P("❌ An error occurred during the test."),
            html.Pre(str(e))
        ])

if __name__ == '__main__':
    app.run(debug=True)
