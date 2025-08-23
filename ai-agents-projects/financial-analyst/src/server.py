from mcp.server.fastmcp import FastMCP

# create FastMCP instance
mcp = FastMCP("Code Runner", port=8081)

@mcp.tool()
def save_code(code: str) -> str:
    """
    Expects a nicely formatted, working and executable python code as input in form of a string.
    Save the given code to a file stock_analysis.py, make sure the code is a valid python file, nicely formatted and ready to execute.

    Args:
        code (str): The nicely formatted, working and executable python code as string.

    Returns:
        str: A message indicating the code was saved successfully.
    """
    try:
        with open("stock_analysis.py", "w") as f:
            f.write(code)
        return "Code saved to stock_analysis.py"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def run_code_and_show_plot() -> str:
    """
    Run the code in stock_analysis.py and generate the plot
    """
    with open("stock_analysis.py", "r") as f:
        exec(f.read())

@mcp.tool()
def run_code_and_save_plot():
    """
    Run the code in stock_analysis.py and save the plot to stock-analysis.svg
    """
    with open("stock_analysis.py", "r") as f:
        exec(f.read())



# Run the server locally
if __name__ == "__main__":
    mcp.run(transport="sse")
