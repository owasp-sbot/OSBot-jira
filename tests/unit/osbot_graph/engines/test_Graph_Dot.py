from gw_bot.helpers.Test_Helper                     import Test_Helper
from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph
from osbot_jira.osbot_graph.Graph import Graph
from osbot_jira.osbot_graph.engines.Graph_Dot       import Graph_Dot
from osbot_jira.osbot_graph.test_data.Sample_Graphs import Sample_Graphs
from osbot_utils.utils.Files                        import file_create


class test_Graph_Dot(Test_Helper):

    def setUp(self):
        super().setUp()
        self.svg_file   = '/tmp/dot_image.svg'
        self.test_graph = Sample_Graphs.simple_dot_file()
        self.graph_dot  = Graph_Dot(self.test_graph)

    def test_render(self):
        print()
        print(self.graph_dot.render())

    def test_render_svg(self):
        result = self.graph_dot.render_svg()
        svg    = result.get('svg')
        if svg:
            file_create(self.svg_file,svg)
        else:
            self.result = result

    def test_sample_dot_graph(self):
        #self.test_graph.add_node('aaa', data={'shape':'box', 'color':'red'})
        #self.graph_dot.set_label('aaaa').set_node_param('shape','box')
        self.result = self.graph_dot.render_svg_to_file(self.svg_file)
        #self.graph_dot.print_dot_code()

    def test_extra_dot_code(self):
        extra_dot = """
                        node [shape=record];
                        struct1 [label="<f0> left|<f1> middle|<f2> right"];
                        struct2 [label="<f0> one|<f1> two"];
                        struct3 [label="hello&#92;nworld |{ b |{c|<here> d|e}| f}| g | h"];
                        struct1:f1 -> struct2:f0;
                        struct1:f2 -> struct3:here;                                                
                    """
        (Graph_Dot().set_layout_engine_dot()
                    .set_extra_dot_code(extra_dot)
                    .render_svg_to_file(self.svg_file))

    def test_node_records(self):
        graph = Graph()
        (
            graph.add_node_record('struct1', '<f0> left|<f1> middle|<f2> right')
                 .add_node_record('struct2', '<f0> one|<f1> two')
                 .add_node_record('struct3', 'hello&#92;nworld |{ b |{c|<here> d|e}| f}| g | h')
                 .add_edge('struct1:f1','struct2:f0')
                 .add_edge('struct1:f2','struct3:here')
         )
        graph_dot=Graph_Dot(graph)
        (
            graph_dot.set_layout_engine_dot()
                     .render_svg_to_file(self.svg_file)
         )
        graph_dot.print_dot_code()

    def test_from_gs_graph(self):
        graph = Graph()
        #graph_name = 'graph_QIN'  # (SOW-18 128 nodes)
        #graph_name = 'graph_YXT' # person-42 (manages, 43 nodes)
        #graph_name = 'graph_CXJ'   # Playbook-2 (103 nodes)
        graph_name = 'graph_SCE'  # PERSON-4 (8 nodes)

        graph_dot = Lambda_Graph().get_graph_dot(graph_name)

        graph_dot.graph.add_node('test', data={'shape':'record', 'label':'<f0> left|<f1> middle|<f2> right'})
        graph_dot.graph.add_edge('test:f2','GUID-4')

        (graph_dot.set_layout_engine_dot()
                  #.set_rank_sep(0.1)
                  .set_size(2)
                  #.set_node_shape_box()
                  #.set_rank_dir('LR')
                  .set_rank_same  (['TEAM-2'  , 'TASK-177', 'GUID-4'])
                  .set_rank_source(['TASK-166', 'a b c'])
                  .set_rank_sink  ([ 'GUILD-8'])
                  .render_svg_to_file(self.svg_file))

        print()
        print(graph_dot.render())

    def test_from_records(self):
        graph_dot = Graph_Dot()
        graph_dot.graph.add_node('aaaa')
        graph_dot.set_layout_engine_dot()
        graph_dot.render_svg_to_file(self.svg_file)

    def test_graph__set_rank__set_label__set_node_params(self):
        graph_dot = Lambda_Graph().get_graph_dot('graph_SCE')

        (graph_dot.set_layout_engine_dot()
                  .set_rank_dir('LR')
                  .set_label('This is a title\n\n')
                  .set_node_params({'shape': 'box','color':'deepskyblue', 'style':'filled'})
                  #.set_node_shape('box').set_node_param('fontcolor', 'blue')
                  .set_rank_same  (['TEAM-2'  , 'TASK-177', 'GUID-4'])
                  .set_rank_source(['TASK-166', 'a b c'])
                  .set_rank_sink  ([ 'GUILD-8'])
                  .render_svg_to_file(self.svg_file))
        graph_dot.print_dot_code()