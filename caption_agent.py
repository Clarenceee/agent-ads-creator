import base64
from openai import OpenAI
from dependencies import Summary


system_prompt = """
  You are a helpful assistant that generates descriptive and engaging captions for images.
  You take into account both the visual content of the image and the user’s input, which may include context, tone, keywords, or intended audience.
  Your response should be a single caption that aligns with the image content and the user's intent.
  Make sure the caption is coherent, relevant to the image, and respects any stylistic or emotional cues given by the user.
  If the image content is ambiguous or open to interpretation, you may infer reasonable context from the user input.
"""

class ImageCaptioner:
    """
    A class to generate image captions using LLM
    """

    def __init__(
        self,
        model_name: str
        # api_key: str = settings.OPENAI_API_KEY
    ):
        """
        Initialize the image summarizer with an AI model

        Args:
            model_name: Name of the AI model to use
            api_key: API key for authentication
        """

        # self._model = OpenAIModel(model_name)
        # self._agent = Agent(
        #     model=self._model,
        #     system_prompt=system_prompt,
        #     result_type=Summary,
        #     model_settings={
        #         # "temperature": 0,
        #         "max_tokens": 200
        #     }
        # )
        self.model_name = model_name
        print(f"Using model : {self.model_name}")
        self.client = OpenAI()


    @staticmethod
    def encode_image(image_path):
      """
      Function to encode image into base64 format
      """
      with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


    def run(
        self,
        image_base64: str,
        user_prompt: str
    ) -> Summary:
        """
        Generate captions using the AI agent

        Args:
            image_base64: Image in base64 encoded format
            prompt: Context of the image

        Returns:
            Structured summary of the caption
        """
        # print(f"User Prompt: {user_prompt}")
        messages = [
          # {"role": "system", "content": system_prompt},
          {
              "role": "user",
              "content": [
                    {
                        "type": "input_text",
                        "text": user_prompt
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}",
                    },
                ]
          }
        ]

        response = self.client.responses.create(
            model=self.model_name,
            input=messages,
        )


        print(f"-------------Output Summary--------------- \n")

        print(f"Text : {response.output[0].content[0].text} \n")
        print(f"Temperature : {response.temperature}")
        print(f"Top-P : {response.top_p}")

        print(f"Input tokens : {response.usage.input_tokens}")
        print(f"Output tokens : {response.usage.output_tokens}")
        print(f"Total tokens : {response.usage.total_tokens}")


        return response.output[0].content[0].text
