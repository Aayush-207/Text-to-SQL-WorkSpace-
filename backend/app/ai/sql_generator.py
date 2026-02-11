"""SQL generation using Gemini AI."""
import json
import re
from typing import Any, Dict, Optional
import google.generativeai as genai

from app.core.config import get_settings
from app.ai.prompt_builder import PromptBuilder
from app.utils.logger import logger


class SQLGenerator:
    """Generate SQL queries using Gemini AI."""

    def __init__(self):
        """Initialize SQL generator."""
        self.settings = get_settings()
        genai.configure(api_key=self.settings.gemini_api_key)
        self.model = genai.GenerativeModel(
            self.settings.gemini_model,
            generation_config=genai.types.GenerationConfig(
                temperature=self.settings.gemini_temperature,
                max_output_tokens=self.settings.gemini_max_tokens,
                response_mime_type="application/json",
            ),
        )

    async def generate_sql(
        self,
        user_query: str,
        schema_metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate SQL query from natural language.

        Args:
            user_query: Natural language query
            schema_metadata: Database schema metadata

        Returns:
            Dictionary with generated SQL and metadata
        """
        try:
            # Build prompt
            prompt = PromptBuilder.build_sql_generation_prompt(user_query, schema_metadata)

            # Generate SQL using Gemini
            response = self.model.generate_content(prompt)

            # Parse response
            response_text = response.text.strip()

            # Extract JSON if wrapped in markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            result = json.loads(response_text)

            logger.info(f"SQL generated successfully: {result.get('type', 'UNKNOWN')}")

            return {
                "success": True,
                "sql": result.get("sql", ""),
                "type": result.get("type", "UNKNOWN"),
                "confidence": result.get("confidence", 0.5),
                "explanation": result.get("explanation", ""),
                "raw_response": result,
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response: {str(e)}")
            return {
                "success": False,
                "error": "Invalid JSON response from AI",
                "raw_response": response_text if 'response_text' in locals() else None,
            }
        except Exception as e:
            logger.error(f"Failed to generate SQL: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }

    async def explain_sql(self, sql_query: str) -> Dict[str, Any]:
        """
        Explain SQL query.

        Args:
            sql_query: SQL query to explain

        Returns:
            Dictionary with explanation
        """
        try:
            prompt = PromptBuilder.build_sql_explanation_prompt(sql_query)

            response = self.model.generate_content(prompt)
            explanation = response.text.strip()

            logger.info("SQL explanation generated successfully")

            return {
                "success": True,
                "explanation": explanation,
            }

        except Exception as e:
            logger.error(f"Failed to explain SQL: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }

    async def optimize_sql(
        self,
        sql_query: str,
        schema_metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Get optimization suggestions for SQL query.

        Args:
            sql_query: SQL query to optimize
            schema_metadata: Database schema metadata

        Returns:
            Dictionary with optimization suggestions
        """
        try:
            prompt = PromptBuilder.build_sql_optimization_prompt(sql_query, schema_metadata)

            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            # Extract JSON if wrapped in markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            result = json.loads(response_text)

            logger.info("SQL optimization suggestions generated successfully")

            return {
                "success": True,
                "issues": result.get("issues", []),
                "optimizations": result.get("optimizations", []),
                "suggested_query": result.get("suggested_query", ""),
            }

        except Exception as e:
            logger.error(f"Failed to optimize SQL: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }


# Global SQL generator instance
sql_generator = SQLGenerator()
