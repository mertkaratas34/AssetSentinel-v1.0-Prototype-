from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from datetime import datetime

class UIManager:
    def __init__(self):
        self.console = Console()

    def create_header(self):
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        
        title = Text("📊 AssetSentinel: Financial Intelligence", style="bold magenta")
        time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        grid.add_row(title, f"[dim]{time_now}[/dim]")
        return Panel(grid, style="white")

    def create_asset_table(self, assets_data):
        table = Table(box=None, expand=True)
        
        table.add_column("Asset", style="cyan", no_wrap=True)
        table.add_column("Price", justify="right", style="green")
        table.add_column("Δ%", justify="right", style="bright_blue")
        table.add_column("Market", justify="center", style="magenta")
        table.add_column("Status", justify="right", style="yellow")
        table.add_column("My Balance", justify="right", style="bright_yellow")
        table.add_column("Value ($)", justify="right", style="bold green")

        for asset in assets_data:
            price_display = f"${asset['price']:,.2f}" if asset.get('price') else "Fetching..."
            balance = asset.get('balance', 0)
            total_value = asset.get('total_value', 0)
            change_pct = asset.get('change_pct')

            if change_pct is None:
                change_display = "—"
            elif change_pct >= 0:
                change_display = Text(f"+{change_pct:,.2f}%", style="bold green")
            else:
                change_display = Text(f"{change_pct:,.2f}%", style="bold red")
            
            table.add_row(
                asset['name'], 
                price_display,
                change_display,
                asset['market'],
                "● Active" if asset.get('price') else "○ Syncing",
                f"{balance:.4f}",
                f"${total_value:,.2f}"
            )
            
        return Panel(table, title="[bold white]Market Overview[/bold white]", border_style="blue")

    def render_dashboard(self, assets_data):
        self.console.clear()
        self.console.print(self.create_header())
        
        # Toplam değeri hesapla
        total_wealth = sum(asset.get('total_value', 0) for asset in assets_data)
        
        # Ana tabloyu bas
        self.console.print(self.create_asset_table(assets_data))
        
        # TOTAL WEALTH PANELİ
        wealth_text = Text.assemble(
            ("TOTAL PORTFOLIO VALUE: ", "bold white"),
            (f"${total_wealth:,.2f}", "bold blink green")
        )
        self.console.print(Panel(Align.center(wealth_text), border_style="bold green"))
        
        self.console.print("\n[dim italic]Press Ctrl+C to exit. Updates every 60s.[/dim italic]", justify="center")