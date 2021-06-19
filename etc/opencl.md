# OpenCL이란? Tensorflow Lite에서 OpenCL을 사용해보자

OpenCL(Open Computing Language)은 개방형 범용 병렬 컴퓨팅 네트워크입니다. OpenCL은 CPU, GPU, DSP 등의 프로세서로 이루어진 이종 플랫폼에서 실행되는 프로그램을 작성할 수 있게 해줍니다. 

애플이 최초로 개발하였는데, AMD, 인텔, 엔비디아 등과 함께 애플이 문서를 다듬어 최초의 제안서를 크로노스 그룹에 제출하게 됩니다. 크로노스 그룹은 비영리 기술 컨소시움으로, 크로노스 그룹 그룹원들이 검토하여 2008년에 처음으로 공식 발표가 됩니다. 

OpenCL을 사용하게되는 이유는 기본적으로 GPU를 사용하기 위해서입니다. 일반적인 컴퓨팅 연산에서 GPU를 사용하게 된다면 CPU-> GPU -> CPU의 순서로 연산의 흐름이 이동하게 되는데 이 과정 속에서도 또 다른 연산이 필요하기 때문에 일반적으로 시간이 더 들죠. 기본적인 제어 흐름은 여전히 CPU에게 맡기고 원래 CPU만을 활용하기 위한 부분에 무언가를 덧대어 GPU에게 명령을 추가하는 방식을 택하기 위한 여러가지 방법들이 개발되었는데 그 중 하나가 바로 이 OpenCL입니다. (다른 대표적인 예로는 CUDA가 있습니다.)

Tensorflow lite에서는 OpenCL에서 연산이 가능하도록 해주는 부분이 들어가 있습니다. 예제 코드로 살펴봅시다!

## 예제 코드

1. git clone 으로 tensorflow 가져오기

```bash
git clone https://github.com/tensorflow/tensorflow.git
```

2. tensorflow 가져온 폴더에서 configuration 진행

```bash
$ ./configure
```

3. `test.cc` 파일 작성 작성

```c
//test.cc

#include <algorithm>
#include <chrono>
#include <iostream>
#include <string>

#include "absl/time/time.h"
#include "tensorflow/lite/delegates/gpu/cl/environment.h"
#include "tensorflow/lite/delegates/gpu/cl/inference_context.h"
#include "tensorflow/lite/delegates/gpu/common/model.h"
#include "tensorflow/lite/delegates/gpu/common/status.h"
#include "tensorflow/lite/delegates/gpu/common/testing/tflite_model_reader.h"
#include "tensorflow/lite/delegates/gpu/delegate.h"
#include "tensorflow/lite/kernels/kernel_util.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"

using namespace std;
using namespace std::chrono;
using namespace tflite;
using namespace tflite::gpu;
using namespace tflite::gpu::cl;

float TimeSinceStartMS(const high_resolution_clock::time_point& start){
    return duration_cast<nanoseconds>(high_resolution_clock::now() - start).count() * 1e-6;
}

int main(int argc, char** argv){
    int kNumRuns = 10;
    int kNumExecutions = 150;

    auto model = FlatFutterModel::BuildFromFile(argv[1]);
    ops::builtin::BuiltinOpResolver op_resolver;
    InterpreterBuilder builder(*model, op_resolver);
    
    std::cout << "Execute GPU Only OpenCL interence." << std::endl;
    GraphFloat32 graph_cl;
    BuildFromFlatBuffer(*model, op_resolver, &graph_cl);

    Environment env;
    CreateEnvironment(&env);

    InferenceContext::CreateInterenceInfo crate_info;
    create_info.precision = env.IsSupport(CalculationsPrecision::F16)
                            ? CalculationsPrecision::F16
                            : CalculationsPrecision::F32;
    create_info.stroage_type = GetFastestStroageType(env.device().GetInfo());
    create_info.hints.Add(ModelHints::kAllowSpecialKernels);
    InferenceContext context;
    context.InitFromGraphWithTransforms(create_info, &graph_cl, &env);
    
    std::cout << "OpenCL GPU-only interence latency" << std::endl;
    auto* queue = env.profilling_queue();
    for (int i=0; i < kNumRuns; ++i){
        const auto start = high_resolution_clock::now();
        for (int k=0; k < kNumExecutions; ++k){
            context.AddToQueue(env.queue());
        }
        env.queue()->WaitForCompletion();
        std::cout << TimeSinceStartMS(start) / kNumExecutions << "ms" << std::endl;
    }

    return EXIT_SUCCESS;
}
```

4. bazel BUILD 파일 작성

```
cc_binary(
    name = "test",
    srcs = ["test.cc"],
    linkopts = [
        "-ldl",
        "-pie",
    ],
    deps = [
        "//tensorflow/lite:framework",
        "//tensorflow/lite/delegates/gpu:delegate",
        "//tensorflow/lite/delegates/gpu/cl:environment",
        "//tensorflow/lite/delegates/gpu/cl:inference_context",
        "//tensorflow/lite/delegates/gpu/common:model",
        "//tensorflow/lite/delegates/gpu/common:status",
        "//tensorflow/lite/delegates/gpu/common/testing:tflite_model_reader",
        "//tensorflow/lite/kernels:builtin_ops",
        "@com_google_absl//absl/time",
    ],
)

```

### Build Start.. 

```bash
$ bazel -c 
```