import os
from typing import Literal

from matplotlib import font_manager, patches, pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from PIL import Image


class Painter:
    @classmethod
    def create_plot(cls, title: str) -> plt.Figure:
        fig = plt.figure(figsize=(20, 25))
        fig.patch.set_facecolor("white")
        fig.suptitle(title, fontsize=30, fontweight="bold", color="black")
        return fig

    @classmethod
    def draw_rectangle(
            cls, ax: Axes, size: Literal["small", "middle", "large"], x_coord: float | int, y_coord: float | int
    ) -> Patch:
        rectangle_sizes = {"small": (1.285, 2), "middle": (1.955, 2.1), "large": (3.975, 1.9)}
        return ax.add_patch(
            patches.Rectangle(
                (x_coord, y_coord), rectangle_sizes[size][0], rectangle_sizes[size][1], facecolor="#f4f4f4"
            )
        )

    @classmethod
    def draw_tests_result_percentage(
            cls, ax: Axes, percentage: str, x_coord: int | float, y_coord: int | float
    ) -> None:
        ax.text(x_coord, y_coord, f"{percentage}%", ha="left", va="center", fontsize=40, color="black")

    @classmethod
    def draw_test_tests_results_count(
            cls, ax: Axes, cases_count: str, x_coord: int | float, y_coord: int | float
    ) -> None:
        ax.text(x_coord, y_coord, f"{cases_count} cases", ha="left", va="center", fontsize=18, color="#575757")

    @classmethod
    def draw_rectangle_title(
            cls, ax: Axes, text: str, color: str, x_coords: int | float, y_coords: int | float
    ) -> None:
        ax.text(x_coords, y_coords, text, ha="left", va="center", fontsize=14, color=color)

    @classmethod
    def draw_colored_line_in_rectangle(
            cls,
            ax: Axes,
            color: str,
            x_coords: list[int | float],
            y_coords: list[int | float],
    ) -> None:
        ax.add_line(Line2D(x_coords, y_coords, color=color, linewidth=3, solid_capstyle="round"))

    @classmethod
    def draw_duration_title_rectangle(cls, ax: Axes, x_coord: int | float, y_coord: int | float) -> None:
        ax.text(x_coord, y_coord, "TESTS DURATION", ha="center", va="top", fontsize=14, color="black")

    @classmethod
    def draw_session_duration_text(
            cls, ax: Axes, execution_time: str, x_coord: int | float, y_coord: int | float
    ) -> None:
        ax.text(x_coord, y_coord, execution_time, ha="center", va="center", fontsize=40, color="black")

    @classmethod
    def draw_duration_rectangle_with_info(
            cls,
            ax: Axes,
            rectangle_size: Literal["small", "middle", "large"],
            duration: str,
            rectangle_coords: list[int | float],
            title_coords: list[int | float],
            duration_coords: list[int | float],
    ) -> None:
        cls.draw_rectangle(ax, rectangle_size, *rectangle_coords)
        cls.draw_duration_title_rectangle(ax, *title_coords)
        cls.draw_session_duration_text(ax, duration, *duration_coords)

    @classmethod
    def draw_rectangle_with_info(
            cls,
            ax: Axes,
            rectangle_size: Literal["small", "middle", "large"],
            title_text: str,
            percent_status_text: str,
            case_count_text: str,
            inside_color: str,
            rectangle_coords: list[int | float],
            line_coords: list[list[int | float]],
            title_coords: list[int | float],
            percent_status_coords: list[int | float],
            case_count_coords: list[int | float],
    ) -> None:
        cls.draw_rectangle(ax, rectangle_size, *rectangle_coords)
        cls.draw_colored_line_in_rectangle(ax, inside_color, *line_coords)
        cls.draw_rectangle_title(ax, title_text, inside_color, *title_coords)
        cls.draw_tests_result_percentage(ax, percent_status_text, *percent_status_coords)
        cls.draw_test_tests_results_count(ax, case_count_text, *case_count_coords)

    @classmethod
    def configure_pie_description(cls, ax: Axes, data: dict, side: Literal["left", "right"], colors: dict) -> None:
        # Теперь порядок в colors строго соответствует данным из Allure
        status_data = dict(zip(colors, cls.get_percentages_from_data(data), strict=True))
        keys = data["number_of_cases"].keys()
        vals = status_data.values()
        counts = data["number_of_cases"].values()
        for result in list(zip(keys, vals, counts, strict=True)):
            if result[1] == 100 and result[2] == 0:
                data["number_of_cases"][result[0]] = data["total_number_of_cases"]

        rectangles_data: dict = {
            "middle": {
                "passed": {
                    "inside_color": f'{colors["passed"]}',
                    "rectangle_coords": [0, 6.0],
                    "line_coords": [[0.175, 0.175], [7.6, 6.65]],
                    "title_coords": [0.25, 7.49],
                    "percent_status_coords": [0.25, 6.88],
                    "case_count_coords": [0.25, 6.38],
                },
                "expected_fail": {
                    "inside_color": f'{colors["expected_fail"]}',
                    "rectangle_coords": [2.017, 6.0],
                    "line_coords": [[2.192, 2.192], [7.6, 6.65]],
                    "title_coords": [2.27, 7.49],
                    "percent_status_coords": [2.27, 6.88],
                    "case_count_coords": [2.27, 6.38],
                },
            },
            "small": {
                "broken": {
                    "inside_color": f'{colors["broken"]}',
                    "rectangle_coords": [0, 3.86],
                    "line_coords": [[0.175, 0.175], [5.51, 4.57]],
                    "title_coords": [0.25, 5.39],
                    "percent_status_coords": [0.25, 4.78],
                    "case_count_coords": [0.25, 4.28],
                },
                "failed": {
                    "inside_color": f'{colors["failed"]}',
                    "rectangle_coords": [1.345, 3.86],
                    "line_coords": [[1.52, 1.52], [5.51, 4.57]],
                    "title_coords": [1.6, 5.39],
                    "percent_status_coords": [1.6, 4.78],
                    "case_count_coords": [1.6, 4.28],
                },
                "skipped": {
                    "inside_color": f'{colors["skipped"]}',
                    "rectangle_coords": [2.69, 3.86],
                    "line_coords": [[2.865, 2.865], [5.51, 4.57]],
                    "title_coords": [2.95, 5.39],
                    "percent_status_coords": [2.95, 4.78],
                    "case_count_coords": [2.95, 4.28],
                },
            },
            "large": {
                "durations": {"rectangle_coords": [0, 1.82], "title_coords": [2, 3.3], "duration_coords": [2, 2.5]}
            },
        }

        for rectangle_size, case_statuses in rectangles_data.items():
            for case_status, case_status_data in case_statuses.items():
                if side == "right":
                    for data_key, config in case_status_data.items():
                        if not isinstance(config, str):
                            if isinstance(config[0], list):
                                right_side_coords = [
                                    [config[0][0] + 4.05, config[0][1] + 4.05],
                                    [config[1][0], config[1][1]],
                                ]
                            else:
                                right_side_coords = [config[0] + 4.05, config[1]]
                            case_status_data[data_key] = right_side_coords
                if rectangle_size != "large":
                    cls.draw_rectangle_with_info(
                        ax,
                        rectangle_size,
                        " ".join(case_status.upper().split("_")),
                        status_data[case_status],
                        data["number_of_cases"][case_status],
                        **rectangles_data[rectangle_size][case_status],
                    )
                else:
                    cls.draw_duration_rectangle_with_info(
                        ax,
                        rectangle_size,
                        data["test_session_duration"],
                        **rectangles_data[rectangle_size]["durations"],
                    )

        ax.set_xlim(0, 8)
        ax.set_ylim(0, 8)
        ax.axis("off")

    @classmethod
    def get_percentages_from_data(cls, data: dict) -> list:
        if data["total_number_of_cases"] == 0 or not any(list(data["number_of_cases"].values())):
            return [0, 0, 100, 0, 0]
        return [round((case / data["total_number_of_cases"]) * 100, 2) for case in data["number_of_cases"].values()]

    @classmethod
    def draw_pie(cls, ax: Axes, cases_percentages: list, colors: dict) -> None:
        edge_color = "none" if cases_percentages[2] == 100 or cases_percentages[3] == 100 else "white"
        ax.pie(
            x=cases_percentages,
            colors=list(colors.values()),
            startangle=90,
            wedgeprops={"width": 0.22, "edgecolor": edge_color},
        )

    @classmethod
    def draw_pie_title(cls, ax: Axes, text: str, size: int, y_coord: int | float) -> None:
        ax.set_title(text, size=size, y=y_coord, color="black", weight="bold")

    @classmethod
    def draw_text(
            cls, ax: Axes, text: str, font_size: int, color: str, weight: str, x_coord: int | float,
            y_coord: int | float
    ) -> None:
        ax.text(x_coord, y_coord, text, ha="center", va="center", fontsize=font_size, color=color, weight=weight)

    @classmethod
    def configure_single_pie(
            cls, data: dict, fig: plt.Figure, gs: object, title: str, subplot: Axes, side: Literal["left", "right"]
    ) -> None:
        ax: Axes = fig.add_subplot(gs)  # type: ignore

        # ИСПРАВЛЕНО: Порядок строго совпадает со словарем statuses из генератора отчетов!
        colors = {
            "passed": "#97cc64",
            "failed": "#fc593e",
            "broken": "#ffd050",
            "skipped": "#a8a8a8",
            "expected_fail": "#d35ebf",
        }
        cases_percentages = cls.get_percentages_from_data(data)
        cls.draw_pie_title(ax, title, 27, 1.05)
        cls.draw_pie(ax, cases_percentages, colors)
        cls.draw_text(ax, f"{cases_percentages[0]}%", 50, "black", "bold", *[0, 0])
        cls.draw_text(ax, f'App Version: {data["application_version"]}', 16, "#575757", "bold", *[0, -1.3])
        cls.draw_text(ax, f'{data["total_number_of_cases"]} cases', 20, "#575757", "bold", *[0, 0.5])
        cls.draw_text(ax, data["test_session_date"], 20, "#575757", "bold", *[0, -0.35])
        ax.axis("equal")
        cls.configure_pie_description(subplot, data, side, colors)

    @classmethod
    def set_font(cls) -> None:
        font_dir = os.path.join(os.getcwd(), "scripts", "chakra_petch_font")
        if os.path.isdir(font_dir):
            for font_file in font_manager.findSystemFonts(fontpaths=[font_dir]):
                font_manager.fontManager.addfont(font_file)
                if "ChakraPetch" in font_file:
                    plt.rcParams["font.family"] = "Chakra Petch"
                    return

    @classmethod
    def create_statistic_image(cls, data: dict, platform: str, stream: str) -> str:
        cls.set_font()
        fig = cls.create_plot(f'[{platform.upper()}] - {" ".join(stream.capitalize().split("_"))}')
        gs = fig.add_gridspec(3, 2, wspace=0.1)
        subplot = fig.add_subplot(gs[1, :])

        cls.configure_single_pie(
            data["today"],
            fig,
            gs[0, 1],
            "Current Test Result",
            subplot,
            "right",
        )
        if len(data) == 2:
            cls.configure_single_pie(
                data["previous"],
                fig,
                gs[0, 0],
                "Previous Test Result",
                subplot,
                "left",
            )

        image_name = "statistic_image.png"
        fig.savefig(image_name)
        Image.open(image_name).crop((230, 0, 1820, 1430)).save(image_name, "PNG")
        return f'Statistic image: "{image_name}" was created successfully'