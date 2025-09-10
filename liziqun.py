
from manim import *
import numpy as np

# 配置参数（学习因子、惯性权重等）
w = 1     # 惯性权重
c1 = 1    # 个体学习因子
c2 = 1    # 群体学习因子
N=3        #参数个数
T_max = 5  # 最大迭代次数
        


class UserScene(Scene):
    def construct(self):
        # 标题
        title = Text("粒子群优化算法 (PSO) 简介", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 创建圆点
        dot = Dot(color=WHITE)
        self.play(FadeIn(dot))  # 先显示圆点
        self.wait(1)

        # 创建箭头，指定不同的方向
        arrow1 = Arrow(start=dot.get_center(),  end=[0.5,3,0], color=RED)  # v
        arrow2 = Arrow(start=[0.5,3,0],         end=[2,3.15,0], color=BLUE)    # 群体投影
        arrow3 = Arrow(start=[2,3.15,0],        end=[3,2.55,0], color=GREEN)  # 个体投影

        arrow4 = DashedLine(start=dot.get_center(), end=[2.5,-1.5,0], dash_length=0.1,color=GREEN)

        arrow5 = DashedLine(start=dot.get_center(), end=[6,0.6,0], dash_length=0.1,color=BLUE)

        arrow=Arrow(start=dot.get_center(),  end=[3,2.55,0], color=YELLOW)
        

        # 让箭头从圆点显现出来
        self.play(GrowArrow(arrow1))  # 红色箭头从圆点生长
        # self.wait(1)
        self.play(Create(arrow5))  
        # self.wait(1)
        self.play(GrowArrow(arrow2))  # 蓝色箭头从圆点生长
        # self.wait(1)
        self.play(Create(arrow4))  
        # self.wait(1)
        self.play(GrowArrow(arrow3))  # 绿色箭头从圆点生长
        # self.wait(1)  # 显示结束后稍微停留

        self.play(GrowArrow(arrow))  # 实际位移路线从圆点生长
        # self.wait(1)

         # 让箭头消失
        self.play(FadeOut(arrow1))  # 红色箭头消失
        self.wait(0.5)
        self.play(FadeOut(arrow2))  # 蓝色箭头消失
        self.wait(0.5)
        self.play(FadeOut(arrow3))  # 绿色箭头消失
        self.wait(2)  # 停留2秒

        self.play(FadeOut(arrow4))
        self.play(FadeOut(arrow5))
        self.play(FadeOut(arrow))
        self.play(FadeOut(dot))
        self.wait(2)

        # ---------------------------
        # 1. 标题与简介
        # ---------------------------
        

        intro_text = Text("以一群“粒子”在解空间中搜索最优解为例，通过\n"
                          "“惯性 + 个体经验 + 群体经验”不断迭代更新", font_size=30)
        self.play(Create(intro_text))
        self.wait(3)
        self.play(FadeOut(intro_text))

        # ---------------------------
        # 2. 初始化参数
        # ---------------------------

        params = VGroup(
            VGroup(Text("粒子数:", font_size=24), Tex(f"$N = {N}$", font_size=30)).arrange(RIGHT, buff=0.5),
            VGroup(Text("维度:", font_size=24), Tex("$D = 2$", font_size=30)).arrange(RIGHT, buff=0.5),
            VGroup(Text("学习因子:", font_size=24), Tex(f"$c_1 = {c1}, \, c_2 = {c2}$", font_size=30)).arrange(RIGHT, buff=0.5),
            VGroup(Text("惯性权重:", font_size=24), Tex(f"$w = {w}$", font_size=30)).arrange(RIGHT, buff=0.5),
            VGroup(Text("最大迭代次数:", font_size=24), Tex(f"$T = {T_max}$", font_size=30)).arrange(RIGHT, buff=0.5),
            VGroup(Text("优化目标(最小化):", font_size=24), Tex("$f(x,y) = x^2 + y^2$", font_size=30)).arrange(RIGHT, buff=0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(params))
        self.wait(5)
        self.play(FadeOut(params))

        # # 惯性项：w * v_old
        # inertia_term = w * velocities[i]
        # # 认知项：c1*r1*(pbest - x_old)
        # cognitive_term = c1 * r1 * (pbest_positions[i] - positions[i])
        # # 社会项：c2*r2*(gbest - x_old)
        # social_term = c2 * r2 * (gbest_position - positions[i])
        params1 = VGroup(
            VGroup(Text("对其中的每一个粒子来说，每次迭代前的速度由以下三部分决定：", font_size=24)).arrange(RIGHT, buff=0.5),
            VGroup(Text("自身速度:", font_size=24), Tex("$w * v[i]$", font_size=30)).arrange(RIGHT, buff=0.5),
            VGroup(Text("群体最优位置对速度的影响:", font_size=24), Tex("$c2 * r2 * (gbest_position - positions[i])$", font_size=30)).arrange(RIGHT, buff=0.5),
            VGroup(Text("个体最优位置对速度的影响:", font_size=24), Tex("$c1 * r1 * (pbest_positions[i] - positions[i])$", font_size=30)).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(params1))
        self.wait(3)
        self.play(FadeOut(params1))

        numberplane = NumberPlane(
            background_line_style={
               "stroke_color": BLUE,"stroke_opacity": 0.3
            },
            axis_config={"color": WHITE}  # 设置坐标轴的颜色
        )
        self.add(numberplane)


        # ---------------------------
        # 3. 初始化粒子：随机位置 + 随机速度
        # ---------------------------
        # 定义优化问题的目标函数（这里用简单的平方和，全局最优(0,0,0)）
        def objective_func(pos):
            x, y, z = pos
            return x**2 + y**2

        # 初始化粒子群
        
        particles = VGroup()
        pbest_positions = []    # 个体历史最优位置
        pbest_fitness = []      # 个体历史最优适应度
        velocities = []         # 粒子速度
        positions = []          # 粒子当前位置

        # 固定显示位置起点，适应度文本在左，个体最优适应度文本在右
        fitness_start = LEFT*4 + UP*3    # 适应度文本从左上角开始
        pbest_start = LEFT*2 + UP*3      # 个体最优适应度文本从左中间开始

        # 每条文本的垂直间距
        vertical_spacing = 0.5


        # 随机生成 N 个粒子的初始位置（2维）、初始速度
        for i in range(N):
            # 随机位置：在 [-5,5] 范围内
            x = np.random.uniform(-3, 3)
            y = np.random.uniform(-3, 3)
            pos = np.array([x, y,0])  # 修改为二维向量
            positions.append(pos)

            # 随机速度：在 [-1,1] 范围内
            vx = np.random.uniform(-1, 1)
            vy = np.random.uniform(-1, 1)
            vel = np.array([vx, vy,0])
            velocities.append(vel)

            # 初始时，个体最优 = 当前位置，适应度 = 当前函数值
            pbest_positions.append(pos.copy())
            pbest_fitness.append(objective_func(pos))

        # 找到群体历史最优（gbest）
        gbest_idx = np.argmin(pbest_fitness)
        gbest_position = pbest_positions[gbest_idx].copy()
        gbest_fitness = pbest_fitness[gbest_idx]

        # 创建粒子（Dot）和速度箭头（Arrow）
        particle_dots = VGroup()
        particle_index=VGroup()
        velocity_arrows = VGroup()
        fitness_texts = VGroup()   # 显示每个粒子的适应度
        pbest_texts = VGroup()    # 显示每个粒子的 pbest 适应度
        gbest_text = VGroup(Text("群体最优：位置 =", font_size=20,color=YELLOW), Tex(f"${gbest_position}$", font_size=30,color=YELLOW),Text(", 适应度 =", font_size=20,color=YELLOW), Tex(f"${gbest_fitness:.2f}$", font_size=30,color=YELLOW)).arrange(RIGHT, buff=0.5).to_edge(UP)
        
        # Text(f"群体最优：位置 = {gbest_position}, 适应度 = {gbest_fitness:.2f}", 
        #                   font_size=20, color=YELLOW).to_edge(UP)

        for i in range(N):
            # 创建粒子（蓝色圆点）
            dot = Dot(point=positions[i], radius=0.15, color=BLUE)
            particle_dots.add(dot)
            number_text = Text(str(i), font_size=20,color=BLACK).move_to(dot.get_center())
            particle_index.add(number_text)

            # 创建速度箭头（从粒子指向 速度方向）
            te=velocities[i]
            vel_arrow = Arrow(
                start=positions[i], 
                end=positions[i] + te/ np.linalg.norm(te),  # 单位向量方便看
                buff=0, color=GREEN
            )
            velocity_arrows.add(vel_arrow)

            # 显示当前适应度
            fit_text = VGroup(Text(f"适应度_{i} =",font_size=20),Tex(f"${objective_func(positions[i]):.2f}$",font_size=25)).arrange(RIGHT, buff=0.5).next_to(fitness_start - i*vertical_spacing*UP, LEFT)
            # Text(f"适应度_{i} = {objective_func(positions[i]):.2f}", 
            #                font_size=16).next_to(dot, UP)
            
            fitness_texts.add(fit_text)

            # 显示个体最优适应度
            pbest_fit_text = Tex(f"$pbest_{i} = {pbest_fitness[i]:.2f}$", 
                                 font_size=25, color=ORANGE).next_to(pbest_start - i*vertical_spacing*UP, LEFT)
            pbest_texts.add(pbest_fit_text)

        # 把所有粒子、箭头、文字加入场景
        self.play(
            Create(particle_dots),
            Create(velocity_arrows),
            Write(fitness_texts),
            Write(pbest_texts),
            Write(gbest_text),
            Create(particle_index)
        )
        self.wait(3)

        # ---------------------------
        # 4. 迭代更新：速度更新 → 位置更新 → 适应度计算 → 更新 pbest/gbest
        # ---------------------------
        
        for t in range(T_max):
            # 每轮迭代前，先“擦除”上一轮的速度箭头、适应度文字、pbest文字，再重新画
            self.play(
                # FadeOut(velocity_arrows),
                FadeOut(fitness_texts),
                FadeOut(pbest_texts)
                # ,
                # FadeOut(particle_index)
            )
            new_velocity_arrows= VGroup()   # 清空箭头对象
            fitness_texts= VGroup()    # 清空适应度文本
            pbest_texts= VGroup()      # 清空最佳位置文本
            # particle_index=VGroup()


            # 遍历每个粒子，更新速度、位置、适应度、pbest/gbest
            for i in range(N):
                # --- (1) 计算新速度 ---
                # 公式：v_new = w*v_old + c1*r1*(pbest - x_old) + c2*r2*(gbest - x_old)
                r1, r2 = np.random.rand(), np.random.rand()  # 随机因子 [0,1]

                # 惯性项：w * v_old
                inertia_term = w * velocities[i]
                # 认知项：c1*r1*(pbest - x_old)
                cognitive_term = c1 * r1 * (pbest_positions[i] - positions[i])
                # 社会项：c2*r2*(gbest - x_old)
                social_term = c2 * r2 * (gbest_position - positions[i])

                # 合成新速度
                new_vel = inertia_term + cognitive_term + social_term
                velocities[i] = new_vel

                # --- (2) 更新位置：x_new = x_old + v_new ---
                new_pos = positions[i] + new_vel
                positions[i] = new_pos

                # --- (3) 计算新适应度 ---
                new_fit = objective_func(new_pos)
                fitness_texts.add(
                    VGroup(Text(f"适应度_{i} = ",font_size=20),Tex(f"${new_fit:.2f}$",font_size=25)).arrange(RIGHT, buff=0.5).next_to(fitness_start - i*vertical_spacing*UP, LEFT)
                    # Text(f"适应度_{i} = {new_fit:.2f}", font_size=16).next_to(positions[i], UP)
                )
                # particle_index.add(
                #     Text(str(i), font_size=20).move_to(positions[i])#粒子编号
                # )

                # --- (4) 更新个体最优 (pbest) ---
                if new_fit < pbest_fitness[i]:
                    pbest_positions[i] = new_pos.copy()
                    pbest_fitness[i] = new_fit
                    pbest_texts.add(
                        Tex(f"$pbest_{i} = {pbest_fitness[i]:.2f}$", 
                             font_size=25, color=ORANGE).next_to(pbest_start - i*vertical_spacing*UP, LEFT)
                    )
                else:
                    pbest_texts.add(
                        Tex(f"$pbest_{i} = {pbest_fitness[i]:.2f}$", 
                             font_size=25, color=ORANGE).next_to(pbest_start - i*vertical_spacing*UP, LEFT)
                    )

                # 创建本轮的速度箭头（可视化新速度）
                # print("11111111",len(velocity_arrows))
                # velocity_arrows[i]=Arrow(start=velocity_arrows[i].get_start(),end=velocity_arrows[i].get_end() + new_vel*0.5,buff=0, color=GREEN)
                new_vel_arrow = Arrow(
                    start=new_pos, 
                    end=new_pos + new_vel*0.5,  # 缩放0.5方便看
                    buff=0, color=GREEN
                )
                new_velocity_arrows.add(new_vel_arrow)#**************************************************

            # --- (5) 更新群体最优 (gbest) ---
            current_gbest_idx = np.argmin(pbest_fitness)
            current_gbest_fit = pbest_fitness[current_gbest_idx]
            if current_gbest_fit < gbest_fitness:
                gbest_position = pbest_positions[current_gbest_idx].copy()
                gbest_fitness = current_gbest_fit

            # 更新 gbest 文字
            new_gbest_text = VGroup(Text("群体最优：位置 =", font_size=20,color=YELLOW), 
                                Tex(f"${gbest_position}$", font_size=30,color=YELLOW),
                                Text(", 适应度 =", font_size=20,color=YELLOW), 
                                Tex(f"${gbest_fitness:.2f}$", font_size=30,color=YELLOW)).arrange(RIGHT, buff=0.5).to_edge(UP)
            # new_gbest_text = Text(
            #     f"群体最优：位置 = {gbest_position}, 适应度 = {gbest_fitness:.2f}", 
            #     font_size=20, color=YELLOW
            # ).to_edge(UP)
            self.play(Transform(gbest_text, new_gbest_text))
            self.wait(1)  # 控制迭代节奏

            # 更新粒子位置、速度箭头、适应度文字、pbest文字
            self.play(FadeOut(velocity_arrows))
            for i in range(len(particle_dots)):
                te=velocities[i]   
                velocity_arrows[i]=Arrow(start=velocity_arrows[i].get_start(),end=te/ np.linalg.norm(te)+velocity_arrows[i].get_start(),buff=0, color=GREEN)
            self.play(Create(velocity_arrows))


            # 逐个移动每个粒子点（Dot）到对应的位置
            animations = []
            for i in range(len(particle_dots)):
                animations.append(particle_dots[i].animate.move_to(positions[i]))
                animations.append(particle_index[i].animate.move_to(positions[i]))
                # animations.append(velocity_arrows[i].animate.move_to(positions[i]))
                velocity_arrows[i].shift(positions[i]-velocity_arrows[i].get_start())


            # self.play(Create(velocity_arrows))
            # 同时播放所有移动动画
            self.play(*animations)
            self.play(
                # particle_dots.animate.move_to([pos for pos in positions]),
                # Create(velocity_arrows),
                # Create(velocity_arrows),#************************************************************************************
                Write(fitness_texts),
                Write(pbest_texts),
                Create(particle_index)
            )
            # velocity_arrows=new_velocity_arrows
            # self.play(Create(velocity_arrows))
            self.wait(1)  # 控制迭代节奏

            # 给粒子画“轨迹线”（从旧位置到新位置）
            if t == 0:
                # 第一次迭代，先创建轨迹线的起点（粒子当前位置）
                trails = VGroup(*[Dot(point=pos, radius=0.05, color=particle_dots[i].color) 
                                 for i, pos in enumerate(positions)])
            else:
                # 后续迭代，更新轨迹线（把粒子新位置加入轨迹）
                for i in range(N):
                    trails[i].move_to(positions[i])

            # self.play(Create(trails))  # 只在第一次创建时播放，后续用MoveToTarget
            self.wait(1)  # 控制迭代节奏

        # ---------------------------
        # 5. 迭代结束，输出最优解 + 可视化轨迹
        # ---------------------------
        # 高亮全局最优粒子（让它的颜色变红）
        best_particle = particle_dots[np.argmin([objective_func(pos) for pos in positions])]
        self.play(best_particle.animate.set_color(RED))

        # 显示最终结果
        result_text = VGroup(Text("迭代结束！最优解：位置 ≈", font_size=20,color=YELLOW), 
                Tex(f"${gbest_position}$", font_size=30,color=YELLOW),
                Text(", 适应度 ≈", font_size=20,color=YELLOW), 
                Tex(f"${gbest_fitness:.2f}$", font_size=30,color=YELLOW)).arrange(RIGHT, buff=0.5).to_edge(DOWN)
        # result_text = Text(
        #     f"迭代结束！最优解：位置 ≈ {gbest_position}, 适应度 ≈ {gbest_fitness:.2f}", 
        #     font_size=30, color=GREEN
        # ).to_edge(DOWN)
        self.play(Write(result_text))
        self.wait(3)

        # 可选：淡化粒子、箭头，只保留轨迹和最优解
        # self.play(
        #     FadeOut(particle_dots),
        #     # FadeOut(new_velocity_arrows),
        #     # FadeOut(new_fitness_texts),
        #     # FadeOut(new_pbest_texts),
        #     FadeOut(gbest_text)
        # )
        # self.play(trails.animate.set_color(BLUE).scale(1.1))  # 轨迹线变明显
        self.wait(3)




# 渲染场景
scene = UserScene()
scene.render()
    