from manim import *
import numpy as np

# 自定义支持中文的LaTeX模板
class ChineseTexTemplate(TexTemplate):
    def __init__(self):
        super().__init__()
        self.add_to_preamble(r"""
\usepackage{ctex}
\usepackage{amsmath}
\usepackage{amssymb}
""")

class AntColonyAlgorithm(Scene):
    def construct(self):
        # 设置中文LaTeX模板
        chinese_template = ChineseTexTemplate()
        
        # 第一部分：介绍
        title = Text("蚁群算法 (Ant Colony Optimization)", font_size=48, color=YELLOW)
        subtitle = Text("一种模拟蚂蚁觅食行为的群体智能算法", font_size=36, color=BLUE)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), Write(subtitle))
        self.wait(20)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # 更详细的介绍
        intro_title = Text("算法背景与特点", font_size=40, color=YELLOW)
        self.play(Write(intro_title))
        self.wait(1)
        self.play(intro_title.animate.to_edge(UP))
        
        intro_text = VGroup(
            Text("• 模拟蚂蚁通过信息素沟通寻找最短路径的行为", font_size=32),
            Text("• 由Marco Dorigo于1992年在其博士论文中提出", font_size=32),
            Text("• 属于群体智能(Swarm Intelligence)算法", font_size=32),
            Text("• 适用于离散组合优化问题", font_size=32),
            Text("• 具有正反馈、分布式计算和自组织特性", font_size=32),
            Text("• 能够有效避免局部最优解", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(UP, buff=1.5)
        
        self.play(Write(intro_text))
        self.wait(20)
        self.play(FadeOut(intro_text), FadeOut(intro_title))

        # 第二部分：蚂蚁行为模拟 - 更详细的解释
        behavior_title = Text("蚂蚁的觅食行为与信息素沟通", font_size=40, color=BLUE)
        self.play(Write(behavior_title))
        self.wait(1)
        self.play(behavior_title.animate.to_edge(UP))
        
        # 创建巢穴和食物
        nest = Circle(radius=0.3, color=YELLOW, fill_opacity=1).shift(LEFT*4)
        nest_label = Text("巢穴", font_size=24).next_to(nest, DOWN)
        food = Circle(radius=0.3, color=GREEN, fill_opacity=1).shift(RIGHT*4)
        food_label = Text("食物", font_size=24).next_to(food, DOWN)
        
        self.play(Create(nest), Write(nest_label))
        self.play(Create(food), Write(food_label))
        
        # 创建两条路径 - 一条短一条长
        path1 = Line(nest.get_right(), food.get_left(), color=WHITE, stroke_width=2)
        path2 = ArcBetweenPoints(nest.get_right(), food.get_left(), angle=PI/2, color=WHITE, stroke_width=2)
        
        # 添加路径长度标签
        path1_label = Text("短路径", font_size=20, color=YELLOW).next_to(path1, UP, buff=0.1)
        path2_label = Text("长路径", font_size=20, color=YELLOW).move_to(path2.point_from_proportion(0.5) + UP * 0.3)
        
        self.play(Create(path1), Create(path2), Write(path1_label), Write(path2_label))
        
        # 创建多只蚂蚁
        ants = VGroup()
        for i in range(4):
            ant = Dot(color=RED, radius=0.08).move_to(nest.get_center())
            ants.add(ant)
        
        self.play(Create(ants))
        self.wait(0.5)
        
        # 蚂蚁选择不同路径
        ant_movements = []
        for i, ant in enumerate(ants):
            if i % 2 == 0:  # 一半蚂蚁选择短路径
                move1 = MoveAlongPath(ant, path1, run_time=2, rate_func=linear)
                move2 = MoveAlongPath(ant, path1, run_time=2, rate_func=linear)  # 返回
                ant_movements.extend([move1, move2])
            else:  # 另一半选择长路径
                move1 = MoveAlongPath(ant, path2, run_time=3, rate_func=linear)
                move2 = MoveAlongPath(ant, path2, run_time=3, rate_func=linear)  # 返回
                ant_movements.extend([move1, move2])
        
        self.play(*ant_movements, run_time=6, lag_ratio=0.5)
        
        # 显示信息素积累过程
        explanation_text = Text("短路径上的信息素积累更快，吸引更多蚂蚁", font_size=28, color=YELLOW)
        explanation_text.to_edge(DOWN)
        self.play(Write(explanation_text))
        
        # 信息素轨迹 - 短路径上的信息素更浓
        pheromone_trail1 = path1.copy().set_color(BLUE).set_stroke(width=8, opacity=0.8)
        pheromone_trail2 = path2.copy().set_color(BLUE).set_stroke(width=4, opacity=0.5)
        
        self.play(
            Create(pheromone_trail1),
            Create(pheromone_trail2),
            run_time=2
        )
        self.wait(2)
        
        # 信息素蒸发效果
        evaporation_text = Text("信息素会随时间蒸发，防止算法过早收敛", font_size=28, color=YELLOW)
        evaporation_text.to_edge(DOWN)
        self.play(ReplacementTransform(explanation_text, evaporation_text))
        
        self.play(
            pheromone_trail1.animate.set_stroke(width=6, opacity=0.6),
            pheromone_trail2.animate.set_stroke(width=2, opacity=0.3),
            run_time=2
        )
        self.wait(20)
        
        self.play(
            FadeOut(ants), 
            FadeOut(pheromone_trail1), 
            FadeOut(pheromone_trail2),
            FadeOut(path1), 
            FadeOut(path2), 
            FadeOut(path1_label),
            FadeOut(path2_label),
            FadeOut(nest_label), 
            FadeOut(food_label),
            FadeOut(nest), 
            FadeOut(food),
            FadeOut(evaporation_text),
            FadeOut(behavior_title)
        )
        # 第三部分：算法公式 - 更详细的解释
        formula_title = Text("蚁群算法数学模型", font_size=40, color=GREEN)
        self.play(Write(formula_title))
        self.wait(1)
        self.play(formula_title.animate.to_edge(UP))

        # 信息素更新公式
        formula_name1 = Text("信息素更新公式", font_size=28, color=YELLOW).to_edge(UP, buff=1.2)
        self.play(Write(formula_name1))

        formula1 = MathTex(
            r"\tau_{ij}(t+1) = (1-\rho)\cdot\tau_{ij}(t) + \sum_{k=1}^{m} \Delta\tau_{ij}^k",
            font_size=36,
            tex_template=chinese_template
        ).shift(UP*0.5)

        formula1_explanation = VGroup(
            Text("• τ_ij: 路径(i,j)上的信息素浓度", font_size=24),
            Text("• ρ: 信息素蒸发率(0<ρ<1)", font_size=24),
            Text("• Δτ_ij^k: 第k只蚂蚁在路径(i,j)上留下的信息素", font_size=24),
            Text("• m: 蚂蚁总数", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(formula1, DOWN, buff=0.5).scale(0.8)

        self.play(Write(formula1))
        self.wait(2)
        self.play(Write(formula1_explanation))
        self.wait(3)

        # 信息素增量公式
        formula_name2 = Text("信息素增量公式", font_size=28, color=YELLOW).to_edge(UP, buff=1.2)
        self.play(
            ReplacementTransform(formula_name1, formula_name2),
            FadeOut(formula1),
            FadeOut(formula1_explanation)
        )

        formula2 = MathTex(
            r"\Delta\tau_{ij}^k = \begin{cases} \frac{Q}{L_k} & \text{如果蚂蚁k经过路径(i,j)} \\ 0 & \text{否则} \end{cases}",
            font_size=36,
            tex_template=chinese_template
        ).shift(UP*0.5)

        formula2_explanation = VGroup(
            Text("• Q: 信息素强度常数", font_size=24),
            Text("• L_k: 蚂蚁k完成路径的总长度", font_size=24),
            Text("• 路径越短，留下的信息素越多", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(formula2, DOWN, buff=0.5).scale(0.8)

        self.play(Write(formula2))
        self.wait(2)
        self.play(Write(formula2_explanation))
        self.wait(3)

        # 转移概率公式
        formula_name3 = Text("路径选择概率公式", font_size=28, color=YELLOW).to_edge(UP, buff=1.2)
        self.play(
            ReplacementTransform(formula_name2, formula_name3),
            FadeOut(formula2),
            FadeOut(formula2_explanation)
        )

        formula3 = MathTex(
            r"p_{ij}^k = \frac{[\tau_{ij}]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{l\in N_k} [\tau_{il}]^\alpha \cdot [\eta_{il}]^\beta}",
            font_size=40,
            tex_template=chinese_template
        ).shift(UP*0.5)

        formula3_explanation = VGroup(
            Text("• p_ij^k: 蚂蚁k从位置i选择路径j的概率", font_size=24),
            Text("• η_ij: 启发式信息，通常为1/d_ij (d_ij是距离)", font_size=24),
            Text("• α: 信息素重要程度参数(α≥0)", font_size=24),
            Text("• β: 启发式信息重要程度参数(β≥0)", font_size=24),
            Text("• N_k: 蚂蚁k下一步可选择的路径集合", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(formula3, DOWN, buff=0.5).scale(0.8)

        self.play(Write(formula3))
        self.wait(2)
        self.play(Write(formula3_explanation))
        self.wait(3)

        # 参数影响说明
        param_title = Text("参数对算法性能的影响", font_size=36).to_edge(UP).shift(DOWN*0.5)
        self.play(
            ReplacementTransform(formula_name3, param_title),
            FadeOut(formula3),
            FadeOut(formula3_explanation)
        )

        param_effects = VGroup(
            Text("• α值过大: 蚂蚁过于依赖信息素，容易陷入局部最优", font_size=28),
            Text("• α值过小: 算法接近随机搜索，收敛速度慢", font_size=28),
            Text("• β值过大: 蚂蚁过于贪心，可能错过全局最优解", font_size=28),
            Text("• β值过小: 忽视启发式信息，搜索效率低下", font_size=28),
            Text("• ρ值过大: 信息素蒸发过快，算法难以收敛", font_size=28),
            Text("• ρ值过小: 信息素积累过多，早期路径影响过大", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.8).next_to(param_title, DOWN, buff=0.5)

        # 👇 整体向下移动 1.0 单位
        param_title.shift(DOWN * 1.0)
        param_effects.shift(DOWN * 1.0)

        self.play(Write(param_effects))
        self.wait(20)

        self.play(FadeOut(param_effects), FadeOut(param_title), FadeOut(formula_title))

        # 第四部分：算法流程 - 更详细的步骤
        process_title = Text("蚁群算法基本流程", font_size=40, color=ORANGE)
        self.play(Write(process_title))
        self.wait(1)
        self.play(process_title.animate.to_edge(UP))
        
        steps = VGroup(
            Text("1. 初始化: 设置参数(α,β,ρ,Q)，放置蚂蚁，初始化信息素", font_size=28),
            Text("2. 构建解: 每只蚂蚁根据概率选择路径，构建完整解", font_size=28),
            Text("3. 评估解: 计算各蚂蚁的路径长度/目标函数值", font_size=28),
            Text("4. 更新信息素: 根据蚂蚁的解质量更新路径信息素", font_size=28),
            Text("5. 蒸发信息素: 所有路径上的信息素按比例蒸发", font_size=28),
            Text("6. 终止检查: 满足终止条件则输出最优解，否则返回步骤2", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=1.2).scale(0.7)
        
        self.play(Write(steps))
        self.wait(2)
        
        # 添加流程图（横向排列）
        flow_steps = [
            ("初始化", BLUE),
            ("构建解", GREEN),
            ("评估解", YELLOW),
            ("更新信息素", ORANGE),
            ("终止检查", RED)
        ]
        
        flow_chart = VGroup()
        for i, (text, color) in enumerate(flow_steps):
            rect = Rectangle(height=0.6, width=1.5, fill_color=color, fill_opacity=0.3)
            label = Text(text, font_size=20)
            step = VGroup(rect, label)
            if i > 0:
                arrow = Arrow(LEFT, RIGHT, buff=0.1).set_length(0.8)
                flow_chart.add(arrow)
            flow_chart.add(step)
        
        flow_chart.arrange(RIGHT, buff=0.1).scale(0.8).to_edge(DOWN, buff=0.5)
        
        self.play(Create(flow_chart), run_time=2)
        self.wait(3)
        
        self.play(FadeOut(steps), FadeOut(flow_chart), FadeOut(process_title))

        # 第五部分：TSP示例 - 更详细的演示
        tsp_title = Text("应用示例: 旅行商问题(TSP)", font_size=40, color=PURPLE)
        self.play(Write(tsp_title))
        self.wait(1)
        self.play(tsp_title.animate.to_edge(UP))
        
        # 问题描述
        problem_desc = Text("寻找访问所有城市一次并返回起点的最短路径", font_size=28, color=YELLOW)
        self.play(Write(problem_desc))
        self.wait(2)
        self.play(problem_desc.animate.to_edge(DOWN))
        
        # 创建城市（调整随机种子避免点太近）
        np.random.seed(43)  # 改变种子避免C3和C8太近
        n_cities = 8
        cities = np.random.rand(n_cities, 2) * 5 - 2.5
        city_dots = VGroup()
        city_labels = VGroup()
        
        for i, (x, y) in enumerate(cities):
            dot = Dot(point=[x, y, 0], color=RED, radius=0.1)
            label = Text(f"C{i+1}", font_size=20).next_to(dot, UP, buff=0.05)
            city_dots.add(dot)
            city_labels.add(label)
        
        self.play(Create(city_dots), Write(city_labels))
        self.wait(1)
        
        # 创建蚂蚁
        ants = VGroup()
        for i in range(4):
            ant = Dot(color=BLUE, radius=0.06).move_to(city_dots[0].get_center())
            ants.add(ant)
        
        self.play(Create(ants))
        self.wait(0.5)
        
        # 模拟多次迭代
        iteration_text = Text("迭代 1", font_size=28, color=YELLOW).to_corner(UR)
        self.play(Write(iteration_text))
        
        # 第一次迭代：蚂蚁随机选择路径
        all_paths = VGroup()
        for ant in ants:
            # 随机生成一条路径
            path_order = [0] + list(np.random.permutation(range(1, n_cities))) + [0]
            ant_path = VGroup()
            
            for i in range(len(path_order)-1):
                start_idx = path_order[i]
                end_idx = path_order[i+1]
                
                line = Line(
                    city_dots[start_idx].get_center(),
                    city_dots[end_idx].get_center(),
                    color=YELLOW,
                    stroke_width=2,
                    stroke_opacity=0.6
                )
                ant_path.add(line)
                
                # 创建路径动画
                self.play(
                    ant.animate.move_to(city_dots[end_idx].get_center()),
                    Create(line),
                    run_time=0.5
                )
            
            all_paths.add(ant_path)
            # 返回起点
            self.play(ant.animate.move_to(city_dots[0].get_center()), run_time=0.3)
        
        self.wait(1)
        
        # 更新迭代次数
        self.play(
            iteration_text.animate.become(Text("迭代 2", font_size=28, color=YELLOW).to_corner(UR))
        )
        
        # 第二次迭代：基于信息素选择路径
        self.play(FadeOut(all_paths))
        
        # 模拟信息素更新后的路径选择（短路径更可能被选择）
        best_path_indices = [0, 3, 1, 5, 2, 7, 4, 6, 0]  # 预设一条较好的路径
        
        for ant in ants:
            # 80%概率选择较好路径，20%概率探索新路径
            if np.random.random() < 0.8:
                path_order = best_path_indices
            else:
                path_order = [0] + list(np.random.permutation(range(1, n_cities))) + [0]
                
            ant_path = VGroup()
            
            for i in range(len(path_order)-1):
                start_idx = path_order[i]
                end_idx = path_order[i+1]
                
                line = Line(
                    city_dots[start_idx].get_center(),
                    city_dots[end_idx].get_center(),
                    color=BLUE,
                    stroke_width=3,
                    stroke_opacity=0.7
                )
                ant_path.add(line)
                
                self.play(
                    ant.animate.move_to(city_dots[end_idx].get_center()),
                    Create(line),
                    run_time=0.5
                )
            
            all_paths.add(ant_path)
            self.play(ant.animate.move_to(city_dots[0].get_center()), run_time=0.3)
        
        self.wait(1)
        
        # 最终最优路径
        self.play(
            FadeOut(all_paths),
            FadeOut(ants),
            iteration_text.animate.become(Text("找到最优路径!", font_size=28, color=GREEN).to_corner(UR))
        )
        
        # 显示最优路径
        optimal_order = [0, 3, 1, 5, 2, 7, 4, 6, 0]
        optimal_path = VGroup()
        
        for i in range(len(optimal_order)-1):
            line = Line(
                city_dots[optimal_order[i]].get_center(),
                city_dots[optimal_order[i+1]].get_center(),
                color=RED,
                stroke_width=5
            )
            optimal_path.add(line)
        
        self.play(Create(optimal_path), run_time=3)
        
        self.wait(20)
        
        self.play(
            FadeOut(optimal_path),
            FadeOut(city_dots),
            FadeOut(city_labels),
            FadeOut(iteration_text),
            FadeOut(tsp_title),
            FadeOut(problem_desc)
        )

        # 第六部分：算法变种和改进
        variants_title = Text("蚁群算法的变种与改进", font_size=40, color=GREEN)
        self.play(Write(variants_title))
        self.wait(1)
        self.play(variants_title.animate.to_edge(UP))
        
        variants = VGroup(
            Text("• 蚁群系统(Ant System, AS) - 原始版本", font_size=28),
            Text("• 精英蚁群系统(Elitist AS) - 强化最优路径信息素", font_size=28),
            Text("• 最大-最小蚂蚁系统(MAX-MIN AS) - 限制信息素范围", font_size=28),
            Text("• 蚁群优化(ACO) - 通用框架", font_size=28),
            Text("• 基于排序的蚁群系统(Rank-based AS) - 按路径质量加权", font_size=28),
            Text("• 连续域蚁群算法(ACOR) - 处理连续优化问题", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.8)
        
        self.play(Write(variants))
        self.wait(20)
        
        self.play(FadeOut(variants), FadeOut(variants_title))

        # 第七部分：优点和应用（分两页显示）
        # 优点部分
        advantages_title = Text("蚁群算法的优势与特点", font_size=40, color=BLUE)
        self.play(Write(advantages_title))
        self.wait(1)
        self.play(advantages_title.animate.to_edge(UP))
        
        advantages = VGroup(
            Text("✓ 正反馈机制: 好的解吸引更多搜索", font_size=28),
            Text("✓ 分布式计算: 蚂蚁独立工作，易于并行", font_size=28),
            Text("✓ 鲁棒性强: 对初始条件和参数不敏感", font_size=28),
            Text("✓ 全局优化: 能够避免局部最优解", font_size=28),
            Text("✓ 自适应性强: 适应动态变化的环境", font_size=28),
            Text("✓ 结合先验知识: 通过启发式信息引导搜索", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.8)
        
        self.play(Write(advantages))
        self.wait(3)
        
        # 应用领域部分（下一页）
        self.play(FadeOut(advantages), FadeOut(advantages_title))
        
        applications_title = Text("实际应用领域", font_size=40, color=GREEN)
        self.play(Write(applications_title))
        self.wait(1)
        self.play(applications_title.animate.to_edge(UP))
        
        applications = VGroup(
            Text("• 旅行商问题(TSP)及其变种", font_size=28),
            Text("• 车辆路径规划(VRP)", font_size=28),
            Text("• 网络路由优化", font_size=28),
            Text("• 作业车间调度", font_size=28),
            Text("• 数据挖掘: 聚类分析、特征选择", font_size=28),
            Text("• 图像处理: 边缘检测、图像分割", font_size=28),
            Text("• 电力系统: 电网规划、负荷分配", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.8)
        
        self.play(Write(applications))
        self.wait(20)
        
        self.play(FadeOut(applications), FadeOut(applications_title))

        # 第八部分：总结与展望
        conclusion_title = Text("总结与展望", font_size=48, color=YELLOW)
        self.play(Write(conclusion_title))
        self.wait(1)
        self.play(conclusion_title.animate.to_edge(UP))
        
        conclusion = VGroup(
            Text("• 模拟自然界蚂蚁的智能觅食行为", font_size=32),
            Text("• 通过信息素实现分布式协同优化", font_size=32),
            Text("• 适合解决复杂组合优化问题", font_size=32),
            Text("• 具有自组织、正反馈和鲁棒性特性", font_size=32),
            Text("• 在实际工程中广泛应用并持续发展", font_size=32),
            Text("• 未来方向: 混合算法、大规模并行、动态环境", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.8)
        
        self.play(Write(conclusion))
        self.wait(4)
        
        # 结束
        end_text = Text("谢谢观看!", font_size=48, color=GOLD)
        self.play(ReplacementTransform(conclusion, end_text))
        self.wait(20)
        
        self.play(FadeOut(end_text), FadeOut(conclusion_title))