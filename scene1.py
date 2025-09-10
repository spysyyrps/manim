from manim import *
import numpy as np
import random

class SA_Introduction(Scene):
    def construct(self):
        chinese_font = "SimHei"
        random.seed(20)      # 固定 Python 的随机数
        np.random.seed(20)   # 固定 NumPy 的随机数

        # ---------------- 第一屏：爬山算法 ----------------
        title = Text("模拟退火算法", font_size=48, color=BLUE, font=chinese_font)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        hill_climbing_text = Text("爬山算法 (Hill Climbing)", font_size=36, color=YELLOW, font=chinese_font)
        hill_climbing_text.next_to(title, DOWN, buff=0.8)
        self.play(Write(hill_climbing_text))

        hc_points = VGroup(
            Text("• 局部搜索算法", font_size=28, font=chinese_font),
            Text("• 每一步选择邻域中更优的解", font_size=28, font=chinese_font),
            Text("• 容易陷入局部最优解", font_size=28, font=chinese_font)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        hc_points.next_to(hill_climbing_text, DOWN, buff=0.5)

        self.play(LaggedStart(*[Write(p) for p in hc_points], lag_ratio=0.4))
        self.wait(5)

        self.play(FadeOut(VGroup(title, hill_climbing_text, hc_points)))

        # 创建函数图像
        axes = Axes(
            x_range=[0, 10],
            y_range=[0, 12],
            axis_config={"color": BLUE},
        )
        
        # 定义一个多峰函数
        def func(x):
            return 2 * np.sin(x) + 3 * np.cos(0.5 * x) + 4
        
        graph = axes.plot(func, color=WHITE, x_range=[0, 10])
        
        # 添加坐标轴标签
        labels = axes.get_axis_labels(
            Text("解空间", font=chinese_font, font_size=24).scale(0.5),
            Text("目标函数值", font=chinese_font, font_size=24).scale(0.5)
        )
        
        # 显示函数图像
        self.play(Create(axes), Write(labels))
        self.play(Create(graph))
        self.wait(1)
        
        # 标记全局最优和局部最优
        global_optimum = Dot(axes.c2p(1.15, func(1.15)), color=GREEN, radius=0.1)
        local_optimum = Dot(axes.c2p(8.61, func(8.61)), color=RED, radius=0.1)
        
        
        global_label = Text("全局最优", font=chinese_font, font_size=24, color=GREEN).next_to(global_optimum, UP)
        local_label = Text("局部最优", font=chinese_font, font_size=24, color=RED).next_to(local_optimum, UP)
        
        self.play(Create(global_optimum), Write(global_label))
        self.play(Create(local_optimum), Write(local_label))
        self.wait(1)
        
        # 展示爬山算法成功找到全局最优的情况
        success_title = Text("爬山算法成功案例", font_size=36, color=GREEN, font=chinese_font)
        success_title.to_edge(UP)
        self.play(Write(success_title))
        
        # 从起点开始
        start_point = Dot(axes.c2p(3.0, func(3.0)), color=YELLOW)
        start_label = Text("起点", font=chinese_font, font_size=20, color=YELLOW).next_to(start_point, DOWN)
        self.play(Create(start_point), Write(start_label))
        self.wait(0.5)
        
        # 模拟爬山过程
        current_x = 3.0
        steps = [3.0, 2.5, 2.0, 1.5, 1.15]
        dots = VGroup(start_point)
        arrows = VGroup()
        
        for i in range(1, len(steps)):
            prev_point = axes.c2p(steps[i-1], func(steps[i-1]))
            next_point = axes.c2p(steps[i], func(steps[i]))
            
            dot = Dot(next_point, color=YELLOW)
            arrow = Arrow(prev_point, next_point, color=YELLOW, buff=0.1)
            
            self.play(Create(arrow), run_time=0.5)
            self.play(Create(dot), run_time=0.5)
            
            dots.add(dot)
            arrows.add(arrow)
        
        self.wait(1)
        
        # 清除成功案例
        self.play(
            FadeOut(dots),
            FadeOut(arrows),
            FadeOut(start_label),
            FadeOut(success_title)
        )
        
        # 展示爬山算法陷入局部最优的情况
        failure_title = Text("爬山算法陷入局部最优", font_size=36, color=RED, font=chinese_font)
        failure_title.to_edge(UP)
        self.play(Write(failure_title))
        
        # 从另一个起点开始
        start_point2 = Dot(axes.c2p(7, func(7)), color=ORANGE)
        start_label2 = Text("起点", font=chinese_font, font_size=20, color=ORANGE).next_to(start_point2, DOWN)
        self.play(Create(start_point2), Write(start_label2))
        self.wait(0.5)
        
        # 模拟爬山过程（陷入局部最优）
        current_x = 7.0
        steps2 = [7.0, 7.5, 8.0, 8.61]
        dots2 = VGroup(start_point2)
        arrows2 = VGroup()
        
        for i in range(1, len(steps2)):
            prev_point = axes.c2p(steps2[i-1], func(steps2[i-1]))
            next_point = axes.c2p(steps2[i], func(steps2[i]))
            
            dot = Dot(next_point, color=ORANGE)
            arrow = Arrow(prev_point, next_point, color=ORANGE, buff=0.1)
            
            self.play(Create(arrow), run_time=0.5)
            self.play(Create(dot), run_time=0.5)
            
            dots2.add(dot)
            arrows2.add(arrow)
                
            # 在陷入局部最优时特别说明
            if abs(current_x - 2.5) < 0.1:
                stuck_text = Text("陷入局部最优!", font=chinese_font, font_size=28, color=RED)
                stuck_text.next_to(local_optimum, DOWN)
                self.play(Write(stuck_text))
                self.wait(1)
                self.play(FadeOut(stuck_text))
        
        self.wait(5)

        # ---------------- 第二屏：模拟退火 ----------------
        self.clear()
        sa_text = Text("模拟退火算法 (Simulated Annealing)", font_size=36, color=GREEN, font=chinese_font)
        self.play(Write(sa_text))

        sa_points = VGroup(
            Text("• 受冶金学中退火过程启发", font_size=28, font=chinese_font),
            Text("• 以一定概率接受较差的解", font_size=28, font=chinese_font),
            Text("• 随着温度降低，接受差解的概率减小", font_size=28, font=chinese_font)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        sa_points.next_to(sa_text, DOWN, buff=0.5)

        self.play(LaggedStart(*[Write(p) for p in sa_points], lag_ratio=0.4))
        self.wait(10)

        self.play(FadeOut(VGroup(sa_text, sa_points)))

        # ---------------- 第三屏：对比表格 ----------------
        comparison_title = Text("对比:", font_size=32, color=PURPLE, font=chinese_font)
        self.play(Write(comparison_title))

        hc_col = VGroup(
            Text("爬山算法", font_size=24, font=chinese_font, color=YELLOW),
            Text("贪婪选择", font_size=20, font=chinese_font),
            Text("易陷入局部最优", font_size=20, font=chinese_font),
            Text("无退火过程", font_size=20, font=chinese_font)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        sa_col = VGroup(
            Text("模拟退火", font_size=24, font=chinese_font, color=GREEN),
            Text("概率接受差解", font_size=20, font=chinese_font),
            Text("可能跳出局部最优", font_size=20, font=chinese_font),
            Text("有温度下降过程", font_size=20, font=chinese_font)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        table = VGroup(hc_col, sa_col).arrange(RIGHT, buff=3)
        comparison_group = VGroup(comparison_title, table).arrange(DOWN, buff=0.8)
        comparison_group.move_to(ORIGIN)

        self.play(FadeIn(comparison_group))
        self.wait(10)
        self.play(FadeOut(comparison_group))

        # ---------------- 第四屏：核心公式 ----------------
        formula_title = Text("模拟退火核心公式", font_size=36, color=BLUE, font=chinese_font)
        formula_title.to_edge(UP)
        self.play(Write(formula_title))

        # 状态转移概率公式
        prob_formula = MathTex(
            "P = \\begin{cases} "
            "1 & \\text{if } E_{\\text{new}} < E_{\\text{old}} \\\\"
            "e^{-\\frac{E_{\\text{new}} - E_{\\text{old}}}{T}} & \\text{if } E_{\\text{new}} \\geq E_{\\text{old}}"
            "\\end{cases}",
            font_size=32
        )
        
        prob_text = Text("状态转移概率:", font_size=28, font=chinese_font, color=YELLOW)
        prob_group = VGroup(prob_text, prob_formula).arrange(DOWN, buff=0.5)
        prob_group.move_to(UP * 0.5)
        
        self.play(Write(prob_text))
        self.play(Write(prob_formula))
        self.wait(5)

        # 温度下降公式
        temp_formula = MathTex(
            "T_{k+1} = \\alpha \\cdot T_k",
            font_size=36
        )
        
        temp_text = Text("温度下降公式:", font_size=28, font=chinese_font, color=YELLOW)
        temp_group = VGroup(temp_text, temp_formula).arrange(DOWN, buff=0.5)
        temp_group.move_to(DOWN * 1)
        
        self.play(Write(temp_text))
        self.play(Write(temp_formula))
        self.wait(5)

        # 添加解释文本
        explanation = Text(
            "其中: T是温度, α是衰减系数(0<α<1), E是能量函数(目标函数)",
            font_size=24,
            font=chinese_font,
            color=GRAY
        )
        explanation.next_to(temp_group, DOWN, buff=0.5)
        self.play(Write(explanation))
        self.wait(10)

        # 可视化概率函数
        self.play(FadeOut(VGroup(prob_group, temp_group, explanation)))
        
        # 绘制概率函数图像
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.2],
            x_length=6,
            y_length=4,
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [0.2, 0.4, 0.6, 0.8, 1.0]},
        ).move_to(ORIGIN)
        
        axes_labels = axes.get_axis_labels(
            x_label=MathTex("\\Delta E / T"),
            y_label=MathTex("P")
        )
        
        self.play(Create(axes), Write(axes_labels))
        
        # 绘制指数衰减曲线
        x_max = 5
        curve = axes.plot(
            lambda x: np.exp(-x) if x > 0 else 1,
            x_range=[0, x_max],
            color=YELLOW
        )
        
        curve_label = MathTex("P = e^{-\\frac{\\Delta E}{T}}", font_size=28).next_to(axes, UP)
        self.play(Create(curve), Write(curve_label))
        
        # 添加说明
        note = Text(
            "当ΔE/T增大时，接受较差解的概率P指数下降",
            font_size=24,
            font=chinese_font,
            color=GREEN
        ).next_to(axes, DOWN, buff=0.5)
        
        self.play(Write(note))
        self.wait(3)
        
        # 展示不同温度下的曲线
        self.play(FadeOut(note), FadeOut(curve_label))
        
        temp_note = Text(
            "温度T对概率函数的影响:",
            font_size=24,
            font=chinese_font,
            color=YELLOW
        ).next_to(axes, UP, buff=0.2)
        
        self.play(Write(temp_note))
        
        # 绘制不同温度下的曲线
        high_temp_curve = axes.plot(
            lambda x: np.exp(-x/2) if x > 0 else 1,
            x_range=[0, x_max],
            color=RED
        )
        
        low_temp_curve = axes.plot(
            lambda x: np.exp(-x*2) if x > 0 else 1,
            x_range=[0, x_max],
            color=BLUE
        )
        
        high_temp_label = Text("高温", font_size=20, font=chinese_font, color=RED).next_to(high_temp_curve.point_from_proportion(0.7), RIGHT)
        low_temp_label = Text("低温", font_size=20, font=chinese_font, color=BLUE).next_to(low_temp_curve.point_from_proportion(0.3), RIGHT)
        
        self.play(Create(high_temp_curve), Write(high_temp_label))
        self.wait(1)
        self.play(Create(low_temp_curve), Write(low_temp_label))
        self.wait(2)
        
        explanation_text = Text(
            "温度越高，接受差解的概率越大，有助于跳出局部最优",
            font_size=22,
            font=chinese_font,
            color=GREEN
        ).next_to(axes, DOWN, buff=0.5)
        
        self.play(Write(explanation_text))
        self.wait(10)
        # ---------------- 第五屏：模拟退火算法寻找函数最低点 ----------------
        self.clear()

        function_formula = MathTex(
            r"f(x) = 3 + 2 \sin(x) + 1.5 \sin(2.5x)", 
            font_size=50
        ).move_to(ORIGIN)

        formula_explanation = Tex(
            "函数:",
            tex_template=TexTemplateLibrary.ctex,
            font_size=30
        ).next_to(function_formula, LEFT)

        self.play(Write(function_formula), Write(formula_explanation))
        self.wait(6)  # 展示3秒
        self.play(FadeOut(function_formula), FadeOut(formula_explanation))  # 淡出公式

        # 创建能量景观
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": BLUE},
        )

        # 定义函数
        def func(x):
            return 3 + 2 * np.sin(x) + 1.5 * np.sin(2.5 * x)

        x_vals = np.linspace(0, 10, 200)
        y_vals = [func(x) for x in x_vals]

        graph = axes.plot_line_graph(
            x_values=x_vals,
            y_values=y_vals,
            line_color=YELLOW,
            stroke_width=4,
            add_vertex_dots=False,
        )

        self.play(Create(axes))
        self.play(Create(graph))

        # 添加坐标轴标签
        x_label = axes.get_x_axis_label(Tex("解空间", tex_template=TexTemplateLibrary.ctex))
        y_label = axes.get_y_axis_label(Tex("能量", tex_template=TexTemplateLibrary.ctex, font_size=24))
        self.play(Write(x_label), Write(y_label))

        # 初始解
        current_x = 6.5
        current_point = Dot(axes.coords_to_point(current_x, func(current_x)), color=RED)
        current_label = Tex("当前解", tex_template=TexTemplateLibrary.ctex, font_size=24).next_to(current_point, UP)
        self.play(Create(current_point), Write(current_label))

        # 温度指示器
        temperature = 10.0
        temp_text = Tex(f"温度: {temperature:.2f}", tex_template=TexTemplateLibrary.ctex, font_size=24).to_corner(UR)
        self.play(Write(temp_text))

        # 全局最优解
        y_min = min(y_vals)
        x_min = x_vals[np.argmin(y_vals)]
        global_optimum_x = x_min
        global_optimum_point = Dot(axes.coords_to_point(global_optimum_x, func(global_optimum_x)), color=GREEN)
        global_optimum_label = Tex("全局最优", tex_template=TexTemplateLibrary.ctex, font_size=24).next_to(global_optimum_point, DOWN)

        # 概率显示区域
        prob_info = VGroup()
        prob_info.to_corner(UL)
        
        # 减少迭代次数到8次
        iterations = 20
        speed_1d5 = 1/2
        # 模拟退火过程
        for i in range(iterations):
            # 生成新解
            new_x = current_x + random.uniform(-1, 1)
            new_x = max(0, min(10, new_x))

            new_point = Dot(axes.coords_to_point(new_x, func(new_x)), color=BLUE)
            new_label = Tex("新解", tex_template=TexTemplateLibrary.ctex, font_size=20).next_to(new_point, UP)

            self.play(Create(new_point), Write(new_label), run_time=1*speed_1d5)

            # 计算能量差
            delta_e = func(new_x) - func(current_x)

            # 计算接受概率
            if delta_e < 0:
                accept_prob = 1.0
            else:
                accept_prob = np.exp(-delta_e / temperature)

            # 显示概率信息
            delta_text = Tex(f"$\\Delta E = {delta_e:.2f}$", font_size=20)
            prob_text = Tex(f"$P(接受) = {accept_prob:.2f}$", font_size=20, tex_template=TexTemplateLibrary.ctex)

            # 清除旧的概率信息
            if len(prob_info) > 0:
                self.play(FadeOut(prob_info), run_time=1*speed_1d5)

            prob_info = VGroup(delta_text, prob_text).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
            self.play(Write(prob_info), run_time=1*speed_1d5)

            # 是否接受
            if delta_e < 0 or random.random() < accept_prob:
                # 接受新解
                accept_text = Tex("接受新解!", tex_template=TexTemplateLibrary.ctex, color=GREEN, font_size=24).to_edge(DOWN)
                self.play(Write(accept_text), run_time=1*speed_1d5)

                # 更新当前点和标签的位置，不改变样式
                new_pos = axes.coords_to_point(new_x, func(new_x))
                self.play(
                    current_point.animate.move_to(new_pos),
                    current_label.animate.next_to(new_pos, UP),
                    FadeOut(new_point),
                    FadeOut(new_label),
                    run_time=1*speed_1d5
                )
                current_x = new_x
                self.play(FadeOut(accept_text), run_time=1*speed_1d5)
            else:
                reject_text = Tex("拒绝新解", tex_template=TexTemplateLibrary.ctex, color=RED, font_size=24).to_edge(DOWN)
                self.play(Write(reject_text), run_time=1*speed_1d5)
                self.play(FadeOut(new_point), FadeOut(new_label), run_time=1*speed_1d5)
                self.play(FadeOut(reject_text), run_time=1*speed_1d5)

            # 降温
            temperature *= 0.85
            new_temp_text = Tex(f"温度: {temperature:.2f}", tex_template=TexTemplateLibrary.ctex, font_size=24).to_corner(UR)
            self.play(Transform(temp_text, new_temp_text), run_time=1*speed_1d5)

            # 每2步展示一次全局最优位置
            if i % 2 == 0:
                self.play(Create(global_optimum_point), Write(global_optimum_label), run_time=1*speed_1d5)
                self.wait(0.5*speed_1d5)
                self.play(FadeOut(global_optimum_point), FadeOut(global_optimum_label), run_time=1*speed_1d5)


        # 最终状态
        final_text = Tex("找到近似最优解!", tex_template=TexTemplateLibrary.ctex, color=GREEN, font_size=36)
        self.play(Write(final_text))
        self.wait(1)
        
        # 显示最终位置和全局最优位置的对比
        self.play(Create(global_optimum_point), Write(global_optimum_label))
        self.wait(1)
        
        # 展示公式
        formula = MathTex(
            r"P = \exp\left(-\frac{\Delta E}{T}\right)", font_size=40
        ).to_edge(RIGHT)

        formula_explanation = Tex(
            "接受更差解的概率随温度降低而减小",
            tex_template=TexTemplateLibrary.ctex,
            font_size=24
        ).next_to(formula, DOWN)

        self.play(Write(formula), Write(formula_explanation))
        self.wait(2)

        # 总结
        summary_text = Tex(
            "模拟退火算法通过控制温度参数，\\\
            以一定概率接受较差解，\\\
            从而有可能跳出局部最优找到全局最优解",
            tex_template=TexTemplateLibrary.ctex,
            font_size=28,
            color=RED
        ).to_edge(UP)

        self.play(Write(summary_text))
        self.wait(3)

        # 结束
        self.play(*[FadeOut(obj) for obj in self.mobjects])