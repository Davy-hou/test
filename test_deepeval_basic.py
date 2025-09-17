from deepeval import assert_test, evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import ContextualRelevancyMetric

@assert_test
def test_llm_context():
    # 创建一个模拟的LLM问答场景
    input_query = "什么是向量数据库？"
    actual_output = "向量数据库是一种专门用于存储和检索向量数据的数据库系统，它能够高效地进行相似性搜索。"
    retrieval_context = [
        "向量数据库是一种特殊的数据库，专门设计用于存储和管理向量数据。",
        "它支持高效的相似性搜索，常用于机器学习和AI应用中。"
    ]
    
    # 创建测试用例
    test_case = LLMTestCase(
        input=input_query,
        actual_output=actual_output,
        retrieval_context=retrieval_context
    )
    
    # 创建上下文相关性评估指标
    metric = ContextualRelevancyMetric(
        threshold=0.7,  # 设置相关性阈值
        model="gpt-4",  # 使用GPT-4进行评估
        include_reason=True  # 包含评估原因
    )
    
    # 使用assert_test进行测试
    assert_test(test_case, [metric])

if __name__ == "__main__":
    test_llm_context()