import os 

# inferential dependency graph keys
pd_key = 'p_'
p_key = 'p'
d_key = 'd'
attr_label = 'label'
attr_color = 'color'
attr_is_prob = 'is_prob'
attr_contains = 'sub_graph'
attr_pd_node = 'pd_node'
attr_id = 'id'
attr_last_ts = 'last_ts'

# time stamp constants
completed_key = 'last_completed'
started_key = 'last_started'

# privacy types
pt_private = 'private'
pt_public = 'public'
pt_unknown = 'unknown_privacy'

# state types
st_stale = 'stale'
st_uptodate = 'uptodate'
st_computing = 'computing'
st_exception = 'exception'
st_not_retained = 'Not retained.'

# job types
compute_key = 'compute_job'
sampler_key = 'sampler_job'
manifold_key = 'manifold_privacy_job'


# other constants
user_all = 'All'
graph_folder = 'graphs'

# plotting constants
data_columns = {"col", "row", "style", "hue", "size"}

if not os.path.isdir(graph_folder):
    os.mkdir(graph_folder)
