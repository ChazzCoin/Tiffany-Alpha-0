import os


# class CheckpointGPT:
#     model = None            # raw_model.state_dict()
#     optimizer = None        # optimizer.state_dict()
#     model_args = None       # model_args
#     iteration_count = None  # iteration_count
#     best_val_loss = None    # best_val_loss
#     fonfigGPT = None        # FonfigGPT

CHECKPOINT_GPT = lambda model_state_dict, optimizer_state_dict, model_args, iter_count, bvl, fonfig: {
                    'model': model_state_dict,
                    'optimizer': optimizer_state_dict,
                    'model_args': model_args,
                    'iteration_count': iter_count,
                    'best_val_loss': bvl,
                    'fonfigGPT': fonfig,
                }

class FonfigGPT:
    init_from = 'resume'  # 'scratch' or 'resume' or 'gpt2*'
    out_dir = '../../out'
    checkpoint_file_name = "ckpt.pt"
    always_save_checkpoint = True  # if True, always save a checkpoint after each eval
    save_count_interval = 50
    train_data_path = None
    val_data_path = None
    eval_interval = 5
    log_interval = 1
    eval_iters = 5
    eval_only = False  # if True, script exits right after the first eval

    # data
    gradient_accumulation_steps = 1  # used to simulate larger batch sizes
    batch_size = 32  # if gradient_accumulation_steps > 1, this is the micro-batch size
    block_size = 64
    # model
    n_layer = 16
    n_head = 16
    n_embd = 32
    dropout = 0.0  # for pretraining 0 is good, for finetuning try 0.1+
    # adamw optimizer
    learning_rate = 2e-4  # max learning rate
    max_iters = 200  # total number of training iterations
    lr_decay_iters = 200
    weight_decay = 1e-2
    beta1 = 0.9
    beta2 = 0.95
    # learning rate decay settings
    decay_lr = True  # whether to decay the learning rate
    warmup_iters = 1  # how many steps to warm up for
      # should be ~= max_iters per Chinchilla
    min_lr = 6e-5  # minimum learning rate, should be ~= learning_rate/10 per Chinchilla
    # DDP settings
    backend = 'nccl'  # 'nccl', 'gloo', etc.
    # system
    device = 'cpu'  # examples: 'cpu', 'cuda', 'cuda:0', 'cuda:1', etc.
    device_type = 'cuda' if 'cuda' in device else 'cpu'  # for later use in torch.autocast
    dtype = 'bfloat16'  # 'float32' or 'bfloat16'
    compile = False  # use PyTorch 2.0 to compile the model to be faster
    ddp = int(os.environ.get('RANK', -1)) != -1 # is this a ddp run?

class Fonfig:
    # hyperparameters
    init_from = 'resume'
    always_save_checkpoint = False
    save_iters = 10
    vocab_size = 0
    train_data = None
    val_data = None
    iter_num = 500
    max_iters = 500
    eval_iters = 5
    eval_interval = 5
    best_val_loss = 1e9
    batch_size = 64 # how many independent sequences will we process in parallel?
    block_size = 256 # what is the maximum context length for predictions?
    learning_rate = 3e-4
    device_type = 'mps'
    device = 'mps'
    # Hardware Performance Settings
    n_embd = 32
    n_head = 16
    n_layer = 16
    dropout = 0.2
    # ------------