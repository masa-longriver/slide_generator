def parse_yaml_structure():
    yaml_content = {
        'LightGBM': [
            {'Abstract': [
                'Gradient Boosting Decision Tree (GBDT) は人気のある機械学習アルゴリズムであり、XGBoost や pGBRT など多くの効果的な実装例がある。',
                'しかし、特徴次元が高くデータサイズが大きい場合、効率性とスケーラビリティは依然として満足のいかないものとなっている。',
                '主要な理由の一つは、各特徴に対して情報ゲインを推定するためにすべてのデータインスタンスをスキャンしなければならないため、非常に時間がかかることである。',
                'この問題に対処するために、2つの新しい技術を提案する：Gradient-based One-Side Sampling (GOSS) と Exclusive Feature Bundling (EFB)。',
                'GOSSでは、勾配の小さいデータインスタンスを大幅に除外し、残りを使用して情報ゲインを推定する。',
                'EFBでは、互いに排他的な特徴をバンドルすることで特徴の数を削減する。最適なバンドルの発見はNP困難であるが、貪欲なアルゴリズムが良好な近似を達成できる。',
                'GOSSとEFBを使用した新しいGBDTの実装をLightGBMと呼ぶ。複数の公開データセットでの実験により、LightGBMはトレーニングプロセスを最大で20倍以上高速化し、ほぼ同じ精度を達成することが示された。'
            ]},
            {'Introduction': [
                'Gradient Boosting Decision Tree (GBDT) は効率性、精度、解釈可能性の点で広く使用される。',
                '大規模データの出現によりGBDTは新たな課題に直面している。特に精度と効率性のトレードオフが問題である。',
                '従来のGBDTの実装は、各特徴に対してすべてのデータインスタンスをスキャンし、情報ゲインを推定するため、計算の複雑さが特徴数とインスタンス数に比例し、大規模データを扱うと時間がかかる。',
                'データインスタンスや特徴の数を削減するためには、非自明な方法が必要であり、ここで2つの新技術GOSSとEFBを提案する。'
            ]},
            {'Preliminaries': [
                {'GBDT and Its Complexity Analysis': [
                    'GBDTは決定木のアンサンブルモデルで、各反復で負の勾配にフィットする。',
                    '最も時間がかかる部分は、分割点を見つけることである。',
                    '事前ソートアルゴリズムとヒストグラムベースのアルゴリズムがある。',
                    'ヒストグラムベースのアルゴリズムはメモリ消費およびトレーニング速度の面でより効率的である。'
                ]},
                {'Related Work': [
                    'XGBoost、pGBRT、scikit-learn、Rのgbmなど多くのGBDTの実装がある。',
                    'データサイズの削減にはダウンサンプリングが一般的であるが、ほとんどの手法がAdaBoostに基づいているため、GBDTには直接適用できない。',
                    '特徴数の削減には弱い特徴のフィルタリングが一般的だが、特徴の冗長性の仮定に強く依存する。',
                    '我々の提案するGOSSとEFBはこれらの限界を克服するものである。'
                ]}
            ]},
            {'Gradient-based One-Side Sampling': [
                {'Algorithm Description': [
                    'GOSSでは、すべての大きな勾配を持つインスタンスを保持し、小さな勾配を持つインスタンスをランダムにサンプリングする。',
                    '小さな勾配を持つデータには定数乗数を導入してデータ分布への影響を補正する。'
                ]},
                {'Theoretical Analysis': [
                    'GOSSはサンプルされた情報ゲインの推定値を用いて分割点を決定し、計算コストを大幅に削減する。',
                    'GOSSはランダムサンプリングよりも優れていることが理論的に証明されている。'
                ]}
            ]},
            {'Exclusive Feature Bundling': [
                {'Greedy Bundling': [
                    '最適なバンドル戦略を見つけるのはNP困難であるため、近似アルゴリズムを用いる。',
                    'グラフ彩色問題に還元し、適度な近似比を持つ貪欲アルゴリズムを使用してバンドルを構築する。'
                ]},
                {'Merge Exclusive Features': [
                    'ヒストグラムベースのアルゴリズムは離散的なビンを使用するので、排他的特徴を異なるビンに配置することでバンドルを構築する。',
                    'こうして作られた特徴バンドルは、個々の特徴と同様に機能する。'
                ]}
            ]},
            {'Experiments': [
                {'Overall Comparison': [
                    'XGBoostおよびLightGBMの基本実装と比較してLightGBMを評価。',
                    '複数の公開データセットでの実験により、LightGBMは最速であり、ほぼ同じ精度を達成する。'
                ]},
                {'Analysis on GOSS': [
                    'GOSSの速度向上と精度について評価。',
                    'SGBと比較し、GOSSがより高精度であることを示す。'
                ]},
                {'Analysis on EFB': [
                    'EFBの速度向上について評価。',
                    'EFBは非常に効果的であり、GBDTトレーニングプロセスを大幅に高速化する。'
                ]}
            ]},
            {'Conclusion': [
                '本論文では、Gradient-based One-Side Sampling (GOSS) と Exclusive Feature Bundling (EFB) を含む新しいGBDTアルゴリズムLightGBMを提案した。',
                '理論的な分析と実験結果を示し、LightGBMがXGBoostおよびSGBを計算速度とメモリ消費の点で大幅に上回ることを確認した。',
                '今後の研究では、GOSSにおけるaとbの最適な選択を検討し、EFBの性能をさらに向上させる予定である。'
            ]}
        ]
    }

    result = []
    
    def add_to_result(index, title, content):
        result.append(f"({index}, {title}, {content})")

    index = 0
    for paper_title, sections in yaml_content.items():
        add_to_result(index, '論文タイトル', paper_title)
        index += 1
        for section in sections:
            for section_title, subsections in section.items():
                add_to_result(index, '章', section_title)
                index += 1
                if isinstance(subsections, list):
                    for item in subsections:
                        if isinstance(item, dict):
                            for subsection_title, subitems in item.items():
                                add_to_result(index, '節', subsection_title)
                                index += 1
                                if isinstance(subitems, list):
                                    for subitem in subitems:
                                        add_to_result(index, '項', subitem)
                                        index += 1
                        else:
                            add_to_result(index, '節', item)
                            index += 1
    return result

result = parse_yaml_structure()