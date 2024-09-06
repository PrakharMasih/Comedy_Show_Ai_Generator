from sqlalchemy import select
from models import Chat, ChatRole
# from finetune import query_data
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import List, Union
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder

import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_messages_roles(self):
        stmt = (
            select(Chat)
            .where(Chat.role.in_([ChatRole.ASSISTANT, ChatRole.USER, ChatRole.SYSTEM]))
            .order_by(Chat.created_at.asc())
        )
        result = await self.db.execute(stmt)
        messages = result.scalars().all()
        return list(messages) if messages else None

    async def get_message_history(self):
        message_history: List[Union[HumanMessage, AIMessage, SystemMessage]] = []
        messages = await self.get_all_messages_roles()
        for message in messages:
            if message.role == ChatRole.USER:
                message_history.append(HumanMessage(content=message.message))
            elif message.role == ChatRole.ASSISTANT:
                message_history.append(AIMessage(content=message.message))
            elif message.role == ChatRole.SYSTEM:
                message_history.append(SystemMessage(content=message.message))
        return message_history

    async def process_chat(self, user_message: str):
        try:
            # Add user message to the database
            await self.add_user_message(user_message)

            # Get chat history
            message_history = await self.get_message_history()

            # Add the new user message to the history
            message_history.append(HumanMessage(content=user_message))

            system_message = """You are a friendly and creative storyteller.
            Your goal is to share amusing anecdotes and scenarios that will entertain readers.
            Focus on crafting engaging dialogue and light-hearted situations that flow naturally.
            It is crucial that you generate content that strictly adheres to OpenAI's terms and conditions.
            Avoid any controversial, offensive, or adult themes. Keep all content family-friendly and suitable for all ages.
            Your responses will be used to generate images and audio, so ensure descriptions are vivid but appropriate.
            Each response should be a complete, entertaining vignette or story that aims to bring joy to readers while remaining fully compliant with OpenAI's content policies.
            """

            # Create a chat prompt template
            prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(system_message),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{input}")
            ])

            # Create the chain
            chain = prompt | ChatOpenAI(model="gpt-4")

            # Run the chain
            response = await chain.ainvoke({
                "history": message_history,
                "input": user_message
            })

            # Extract the content from the response
            response = response.content
            # Add assistant response to the database
            await self.add_assistant_message(response)

            return response

        except Exception as e:
            raise

    async def add_message(self, role: ChatRole, content: str):
        message = Chat(role=role, message=content)
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def add_user_message(self, content: str):
        return await self.add_message(ChatRole.USER, content)

    async def add_assistant_message(self, content: str):
        return await self.add_message(ChatRole.ASSISTANT, content)