import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def generate_chart(df: pd.DataFrame, question: str) -> go.Figure:
    if df is None or df.empty:
        return None

    cols = df.columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()
    str_cols = df.select_dtypes(include='object').columns.tolist()
    date_cols = [c for c in cols if 'date' in c.lower()
                 or 'month' in c.lower()]

    # Line chart: has year AND month columns
    if 'year' in cols and 'month' in cols and len(num_cols) >= 1:
        df['period'] = df['year'].astype(
            str) + '-' + df['month'].astype(str).str.zfill(2)
        fig = px.line(
            df,
            x='period',
            y=num_cols[-1],
            title=question,
            markers=True
        )
        return fig

    # Multi-line chart: date/month column + multiple numeric columns
    if len(date_cols) >= 1 and len(num_cols) >= 2:
        fig = go.Figure()
        x_col = date_cols[0]
        for col in num_cols:
            fig.add_trace(go.Bar(name=col, x=df[x_col], y=df[col]))
        fig.update_layout(
            barmode='group',
            title=question,
            xaxis_title=x_col
        )
        return fig

    # Bar chart: one text column + one number column
    if len(str_cols) == 1 and len(num_cols) == 1:
        fig = px.bar(
            df,
            x=str_cols[0],
            y=num_cols[0],
            title=question,
            color=str_cols[0],
            text=num_cols[0]
        )
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(showlegend=False)
        return fig

    # Bar chart: one text column + multiple number columns
    if len(str_cols) >= 1 and len(num_cols) >= 2:
        fig = go.Figure()
        x_col = str_cols[0]
        for col in num_cols:
            fig.add_trace(go.Bar(name=col, x=df[x_col], y=df[col]))
        fig.update_layout(barmode='group', title=question)
        return fig

    # Fallback: bar chart
    if len(num_cols) >= 1 and len(cols) >= 2:
        fig = px.bar(df, x=cols[0], y=num_cols[0], title=question)
        return fig

    return None


if __name__ == "__main__":
    test_df = pd.DataFrame({
        'name': ['Rent', 'Groceries', 'Shopping'],
        'total_amount': [75000, 25500, 23000]
    })

    fig = generate_chart(test_df, "Top 3 expense categories")
    if fig:
        fig.show()
        print("Chart generated successfully!")
