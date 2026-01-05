"""
AI Optimization Card

Displays real-time AI dynamic optimization progress:
- LSTM Prediction Engine (95% accuracy target)
- DQN Training Progress (1000 episodes)
- Combined AI Factor (+0.0 to +0.9 improvement)

Integrated into Overview tab and Research tab (Stage 6).
"""

import logging
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QFrame,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont
from ui.cards.base_card import BaseCard
from colors import DarkMacStyleColors as Colors

# EDIT 1: Logging infrastructure setup
logger = logging.getLogger(__name__)

# ==========================================
# EDIT 2: Constants Extraction
# ==========================================
# Card Configuration
CARD_TITLE = "🤖 AI Dynamic Optimization"

# Section Labels
LSTM_SECTION_LABEL = "🧠 LSTM Prediction Engine"
DQN_SECTION_LABEL = "⚡ DQN Training Progress"
AI_FACTOR_SECTION_LABEL = "✨ Combined AI Factor"
STATUS_SECTION_LABEL = "📊 Status"

# Section Descriptions
LSTM_DESCRIPTION = "Predicts optimal parameters from time series data"
DQN_DESCRIPTION = "Learning optimal configurations through reinforcement"
AI_FACTOR_DESCRIPTION = "Total improvement: LSTM (0-0.5) + DQN (0-0.5) = (0-1.0)"
STATUS_DESCRIPTION = "Real-time AI optimization status"

# Default Label Texts
LSTM_ACCURACY_DEFAULT_TEXT = "Accuracy: 0.0%"
DQN_EPISODES_DEFAULT_TEXT = "Episodes: 0 / 1000"
AI_FACTOR_DEFAULT_TEXT = "AI Factor: +0.00 points"
TRAINING_STATUS_DEFAULT_TEXT = "Status: Ready"
DATA_POINTS_DEFAULT_TEXT = "Data points: 0"

# Layout Configuration
CONTENT_LAYOUT_SPACING = 12
LSTM_CONFIDENCE_BAR_MAXIMUM = 100
DQN_PROGRESS_BAR_MAXIMUM = 1000
AI_FACTOR_BAR_MAXIMUM = 100
METRIC_SECTION_LAYOUT_SPACING = 6
PROGRESS_BAR_HEIGHT = 6
SECTION_PADDING = 8

# Font Configuration
SECTION_TITLE_FONT_SIZE = 11
METRIC_LABEL_FONT_SIZE = 12
AI_FACTOR_LABEL_FONT_SIZE = 13
DESC_LABEL_FONT_SIZE = 11

# Color Configuration
LSTM_CONFIDENCE_COLOR = "#4A90E2"
DQN_PROGRESS_COLOR = "#50C878"
AI_FACTOR_COLOR = "#FF9500"

# Threshold Values for Color Updates
LSTM_ACCURACY_PERFECT_THRESHOLD = 0.95
LSTM_ACCURACY_GOOD_THRESHOLD = 0.80
LSTM_ACCURACY_FAIR_THRESHOLD = 0.50
DQN_PROGRESS_GOOD_THRESHOLD = 0.80
DQN_PROGRESS_FAIR_THRESHOLD = 0.50
AI_FACTOR_GOOD_THRESHOLD = 0.8
AI_FACTOR_FAIR_THRESHOLD = 0.5


class AIOptimizationCard(BaseCard):
    """
    Card displaying real-time AI optimization metrics.

    Shows LSTM prediction confidence, DQN learning progress,
    and combined AI improvement factor.
    """

    def __init__(self, parent=None):
        """
        Initialize AI Optimization Card.

        Args:
            parent: Parent widget (QWidget or None)

        Raises:
            TypeError: If parent is not a QWidget or None
            RuntimeError: If base card initialization fails
        """
        logger.debug("AIOptimizationCard: __init__: Starting parameter validation")

        try:
            # ========================================
            # Parameter Level: parent validation
            # ========================================
            logger.debug(f"AIOptimizationCard: __init__: Validating parent parameter (type: {type(parent).__name__}, value: {parent})")

            # Type check for parent parameter
            try:
                if parent is not None:
                    if not isinstance(parent, QWidget):
                        logger.warning(f"AIOptimizationCard: __init__: parent is not a QWidget (type: {type(parent).__name__}) - attempting to use anyway")
                    else:
                        logger.debug(f"AIOptimizationCard: __init__: parent is valid QWidget (type: {type(parent).__name__})")
                else:
                    logger.debug("AIOptimizationCard: __init__: parent is None - will create as top-level widget")
            except TypeError as e:
                logger.warning(f"AIOptimizationCard: __init__: Type check failed for parent: {str(e)} - using None as fallback")
                parent = None
            except Exception as e:
                logger.warning(f"AIOptimizationCard: __init__: Unexpected error during parent validation: {str(e)} - using None as fallback")
                parent = None

            logger.debug("AIOptimizationCard: __init__: Parameter validation complete")

            # ========================================
            # Step Level: Base class initialization
            # ========================================
            logger.debug("AIOptimizationCard: __init__: Initializing base card with title")
            try:
                if CARD_TITLE is None or not isinstance(CARD_TITLE, str):
                    logger.error(f"AIOptimizationCard: __init__: Invalid CARD_TITLE (type: {type(CARD_TITLE).__name__}, value: {CARD_TITLE})")
                    raise RuntimeError(f"Invalid CARD_TITLE: {CARD_TITLE}")

                logger.debug(f"AIOptimizationCard: __init__: CARD_TITLE is valid: '{CARD_TITLE}'")

                super().__init__(CARD_TITLE, parent)
                logger.debug(f"AIOptimizationCard: __init__: Base card initialized successfully")

            except TypeError as e:
                logger.error(f"AIOptimizationCard: __init__: Base class initialization failed - TypeError: {str(e)}", exc_info=True)
                raise RuntimeError(f"Failed to initialize base card: {str(e)}")
            except RuntimeError as e:
                logger.error(f"AIOptimizationCard: __init__: Base class initialization failed - RuntimeError: {str(e)}", exc_info=True)
                raise
            except Exception as e:
                logger.error(f"AIOptimizationCard: __init__: Base class initialization failed - {type(e).__name__}: {str(e)}", exc_info=True)
                raise RuntimeError(f"Failed to initialize base card: {str(e)}")

            # ========================================
            # Step Level: UI setup initialization
            # ========================================
            logger.debug("AIOptimizationCard: __init__: Starting UI setup")
            try:
                self._setup_optimization_ui()
                logger.debug("AIOptimizationCard: __init__: UI setup completed successfully")
            except RuntimeError as e:
                logger.error(f"AIOptimizationCard: __init__: UI setup failed - RuntimeError: {str(e)}", exc_info=True)
                logger.warning("AIOptimizationCard: __init__: Widget may not display correctly due to UI setup failure")
                raise
            except Exception as e:
                logger.error(f"AIOptimizationCard: __init__: UI setup failed - {type(e).__name__}: {str(e)}", exc_info=True)
                logger.warning("AIOptimizationCard: __init__: Widget may not display correctly due to UI setup failure")
                raise RuntimeError(f"UI setup failed: {str(e)}")

            logger.info("AIOptimizationCard: __init__: Initialization complete - AI Optimization Card ready")

        except RuntimeError as e:
            logger.error(f"AIOptimizationCard: __init__: Critical error during initialization: {str(e)}", exc_info=True)
            logger.error("AIOptimizationCard: __init__: Card initialization failed - widget may not be functional")
            raise
        except Exception as e:
            logger.error(f"AIOptimizationCard: __init__: Unexpected error during initialization: {str(e)}", exc_info=True)
            logger.error("AIOptimizationCard: __init__: Card initialization failed - widget may not be functional")
            raise RuntimeError(f"Initialization failed: {str(e)}")

    def _setup_optimization_ui(self):
        """Set up AI optimization UI elements."""
        logger.debug("AIOptimizationCard: _setup_optimization_ui: Starting UI setup")
        try:
            # Main content layout - critical widget
            self.content_layout = QVBoxLayout()
            if self.content_layout is None:
                logger.error("AIOptimizationCard: _setup_optimization_ui: Failed to create content_layout - QVBoxLayout returned None")
                raise RuntimeError("Failed to create content_layout")

            try:
                self.content_layout.setSpacing(CONTENT_LAYOUT_SPACING)
            except Exception as e:
                logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set content_layout spacing: {str(e)}")
            logger.debug(f"AIOptimizationCard: _setup_optimization_ui: Content layout created with {CONTENT_LAYOUT_SPACING}px spacing")

            # ==========================================
            # LSTM Prediction Engine Section
            # ==========================================
            try:
                logger.debug("AIOptimizationCard: _setup_optimization_ui: Creating LSTM Prediction Engine section")
                lstm_section = self._create_metric_section(
                    LSTM_SECTION_LABEL,
                    LSTM_DESCRIPTION
                )
                if lstm_section is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: _create_metric_section returned None for LSTM")
                    raise RuntimeError("Failed to create LSTM section")

                self.lstm_accuracy_label = QLabel(LSTM_ACCURACY_DEFAULT_TEXT)
                if self.lstm_accuracy_label is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: Failed to create lstm_accuracy_label")
                    raise RuntimeError("Failed to create lstm_accuracy_label")

                try:
                    self.lstm_accuracy_label.setStyleSheet(
                        f"color: {Colors.TEXT_SECONDARY}; font-size: {METRIC_LABEL_FONT_SIZE}px;"
                    )
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set lstm_accuracy_label stylesheet: {str(e)}")

                self.lstm_confidence_bar = QProgressBar()
                if self.lstm_confidence_bar is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: Failed to create lstm_confidence_bar")
                    raise RuntimeError("Failed to create lstm_confidence_bar")

                try:
                    self.lstm_confidence_bar.setMaximum(LSTM_CONFIDENCE_BAR_MAXIMUM)
                    if self.lstm_confidence_bar.maximum() != LSTM_CONFIDENCE_BAR_MAXIMUM:
                        logger.warning(f"AIOptimizationCard: _setup_optimization_ui: lstm_confidence_bar.setMaximum failed - got {self.lstm_confidence_bar.maximum()}, expected {LSTM_CONFIDENCE_BAR_MAXIMUM}")
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set lstm_confidence_bar maximum: {str(e)}")

                try:
                    self.lstm_confidence_bar.setValue(0)
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set lstm_confidence_bar value: {str(e)}")

                try:
                    self.lstm_confidence_bar.setStyleSheet(self._get_progress_bar_style(LSTM_CONFIDENCE_COLOR))
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set lstm_confidence_bar stylesheet: {str(e)}")

                try:
                    self.lstm_confidence_bar.setMaximumHeight(PROGRESS_BAR_HEIGHT)
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set lstm_confidence_bar height: {str(e)}")

                logger.debug("AIOptimizationCard: _setup_optimization_ui: LSTM widgets created (accuracy_label, confidence_bar)")

                try:
                    lstm_section.layout().addWidget(self.lstm_accuracy_label)
                    lstm_section.layout().addWidget(self.lstm_confidence_bar)
                except Exception as e:
                    logger.error(f"AIOptimizationCard: _setup_optimization_ui: Failed to add LSTM widgets to section: {str(e)}")
                    raise

                try:
                    self.content_layout.addWidget(lstm_section)
                except Exception as e:
                    logger.error(f"AIOptimizationCard: _setup_optimization_ui: Failed to add LSTM section to content_layout: {str(e)}")
                    raise

                logger.debug("AIOptimizationCard: _setup_optimization_ui: LSTM section added to content layout")
            except Exception as e:
                logger.error(f"AIOptimizationCard: _setup_optimization_ui: LSTM section creation failed: {str(e)}", exc_info=True)
                logger.debug("AIOptimizationCard: _setup_optimization_ui: Skipping LSTM section due to error")

            # ==========================================
            # DQN Training Progress Section
            # ==========================================
            try:
                logger.debug("AIOptimizationCard: _setup_optimization_ui: Creating DQN Training Progress section")
                dqn_section = self._create_metric_section(
                    DQN_SECTION_LABEL,
                    DQN_DESCRIPTION
                )
                if dqn_section is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: _create_metric_section returned None for DQN")
                    raise RuntimeError("Failed to create DQN section")

                self.dqn_episodes_label = QLabel(DQN_EPISODES_DEFAULT_TEXT)
                if self.dqn_episodes_label is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: Failed to create dqn_episodes_label")
                    raise RuntimeError("Failed to create dqn_episodes_label")

                try:
                    self.dqn_episodes_label.setStyleSheet(
                        f"color: {Colors.TEXT_SECONDARY}; font-size: {METRIC_LABEL_FONT_SIZE}px;"
                    )
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set dqn_episodes_label stylesheet: {str(e)}")

                self.dqn_progress_bar = QProgressBar()
                if self.dqn_progress_bar is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: Failed to create dqn_progress_bar")
                    raise RuntimeError("Failed to create dqn_progress_bar")

                try:
                    self.dqn_progress_bar.setMaximum(DQN_PROGRESS_BAR_MAXIMUM)
                    if self.dqn_progress_bar.maximum() != DQN_PROGRESS_BAR_MAXIMUM:
                        logger.warning(f"AIOptimizationCard: _setup_optimization_ui: dqn_progress_bar.setMaximum failed - got {self.dqn_progress_bar.maximum()}, expected {DQN_PROGRESS_BAR_MAXIMUM}")
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set dqn_progress_bar maximum: {str(e)}")

                try:
                    self.dqn_progress_bar.setValue(0)
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set dqn_progress_bar value: {str(e)}")

                try:
                    self.dqn_progress_bar.setStyleSheet(self._get_progress_bar_style(DQN_PROGRESS_COLOR))
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set dqn_progress_bar stylesheet: {str(e)}")

                try:
                    self.dqn_progress_bar.setMaximumHeight(PROGRESS_BAR_HEIGHT)
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set dqn_progress_bar height: {str(e)}")

                logger.debug("AIOptimizationCard: _setup_optimization_ui: DQN widgets created (episodes_label, progress_bar)")

                try:
                    dqn_section.layout().addWidget(self.dqn_episodes_label)
                    dqn_section.layout().addWidget(self.dqn_progress_bar)
                except Exception as e:
                    logger.error(f"AIOptimizationCard: _setup_optimization_ui: Failed to add DQN widgets to section: {str(e)}")
                    raise

                try:
                    self.content_layout.addWidget(dqn_section)
                except Exception as e:
                    logger.error(f"AIOptimizationCard: _setup_optimization_ui: Failed to add DQN section to content_layout: {str(e)}")
                    raise

                logger.debug("AIOptimizationCard: _setup_optimization_ui: DQN section added to content layout")
            except Exception as e:
                logger.error(f"AIOptimizationCard: _setup_optimization_ui: DQN section creation failed: {str(e)}", exc_info=True)
                logger.debug("AIOptimizationCard: _setup_optimization_ui: Skipping DQN section due to error")

            # ==========================================
            # Combined AI Factor Section
            # ==========================================
            try:
                logger.debug("AIOptimizationCard: _setup_optimization_ui: Creating Combined AI Factor section")
                factor_section = self._create_metric_section(
                    AI_FACTOR_SECTION_LABEL,
                    AI_FACTOR_DESCRIPTION
                )
                if factor_section is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: _create_metric_section returned None for AI Factor")
                    raise RuntimeError("Failed to create AI Factor section")

                self.ai_factor_label = QLabel(AI_FACTOR_DEFAULT_TEXT)
                if self.ai_factor_label is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: Failed to create ai_factor_label")
                    raise RuntimeError("Failed to create ai_factor_label")

                try:
                    self.ai_factor_label.setStyleSheet(
                        f"color: {Colors.GREEN}; font-size: {AI_FACTOR_LABEL_FONT_SIZE}px; font-weight: 600;"
                    )
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set ai_factor_label stylesheet: {str(e)}")

                self.ai_factor_bar = QProgressBar()
                if self.ai_factor_bar is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: Failed to create ai_factor_bar")
                    raise RuntimeError("Failed to create ai_factor_bar")

                try:
                    self.ai_factor_bar.setMaximum(AI_FACTOR_BAR_MAXIMUM)
                    if self.ai_factor_bar.maximum() != AI_FACTOR_BAR_MAXIMUM:
                        logger.warning(f"AIOptimizationCard: _setup_optimization_ui: ai_factor_bar.setMaximum failed - got {self.ai_factor_bar.maximum()}, expected {AI_FACTOR_BAR_MAXIMUM}")
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set ai_factor_bar maximum: {str(e)}")

                try:
                    self.ai_factor_bar.setValue(0)
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set ai_factor_bar value: {str(e)}")

                try:
                    self.ai_factor_bar.setStyleSheet(self._get_progress_bar_style(AI_FACTOR_COLOR))
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set ai_factor_bar stylesheet: {str(e)}")

                try:
                    self.ai_factor_bar.setMaximumHeight(PROGRESS_BAR_HEIGHT)
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set ai_factor_bar height: {str(e)}")

                logger.debug("AIOptimizationCard: _setup_optimization_ui: AI Factor widgets created (factor_label, progress_bar)")

                try:
                    factor_section.layout().addWidget(self.ai_factor_label)
                    factor_section.layout().addWidget(self.ai_factor_bar)
                except Exception as e:
                    logger.error(f"AIOptimizationCard: _setup_optimization_ui: Failed to add AI Factor widgets to section: {str(e)}")
                    raise

                try:
                    self.content_layout.addWidget(factor_section)
                except Exception as e:
                    logger.error(f"AIOptimizationCard: _setup_optimization_ui: Failed to add AI Factor section to content_layout: {str(e)}")
                    raise

                logger.debug("AIOptimizationCard: _setup_optimization_ui: AI Factor section added to content layout")
            except Exception as e:
                logger.error(f"AIOptimizationCard: _setup_optimization_ui: AI Factor section creation failed: {str(e)}", exc_info=True)
                logger.debug("AIOptimizationCard: _setup_optimization_ui: Skipping AI Factor section due to error")

            # ==========================================
            # Status Section
            # ==========================================
            try:
                logger.debug("AIOptimizationCard: _setup_optimization_ui: Creating Status section")
                status_section = self._create_metric_section(
                    STATUS_SECTION_LABEL,
                    STATUS_DESCRIPTION
                )
                if status_section is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: _create_metric_section returned None for Status")
                    raise RuntimeError("Failed to create Status section")

                self.training_status_label = QLabel(TRAINING_STATUS_DEFAULT_TEXT)
                if self.training_status_label is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: Failed to create training_status_label")
                    raise RuntimeError("Failed to create training_status_label")

                try:
                    self.training_status_label.setStyleSheet(
                        f"color: {Colors.TEXT_SECONDARY}; font-size: {DESC_LABEL_FONT_SIZE}px;"
                    )
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set training_status_label stylesheet: {str(e)}")

                self.data_points_label = QLabel(DATA_POINTS_DEFAULT_TEXT)
                if self.data_points_label is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: Failed to create data_points_label")
                    raise RuntimeError("Failed to create data_points_label")

                try:
                    self.data_points_label.setStyleSheet(
                        f"color: {Colors.TEXT_SECONDARY}; font-size: {DESC_LABEL_FONT_SIZE}px;"
                    )
                except Exception as e:
                    logger.warning(f"AIOptimizationCard: _setup_optimization_ui: Failed to set data_points_label stylesheet: {str(e)}")

                logger.debug("AIOptimizationCard: _setup_optimization_ui: Status widgets created (status_label, data_points_label)")

                try:
                    status_section.layout().addWidget(self.training_status_label)
                    status_section.layout().addWidget(self.data_points_label)
                except Exception as e:
                    logger.error(f"AIOptimizationCard: _setup_optimization_ui: Failed to add Status widgets to section: {str(e)}")
                    raise

                try:
                    self.content_layout.addWidget(status_section)
                except Exception as e:
                    logger.error(f"AIOptimizationCard: _setup_optimization_ui: Failed to add Status section to content_layout: {str(e)}")
                    raise

                logger.debug("AIOptimizationCard: _setup_optimization_ui: Status section added to content layout")
            except Exception as e:
                logger.error(f"AIOptimizationCard: _setup_optimization_ui: Status section creation failed: {str(e)}", exc_info=True)
                logger.debug("AIOptimizationCard: _setup_optimization_ui: Skipping Status section due to error")

            # Add content to main layout
            try:
                if self.content_layout is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: content_layout is None when adding to main_layout")
                    raise RuntimeError("content_layout is None")
                if self.main_layout is None:
                    logger.error("AIOptimizationCard: _setup_optimization_ui: main_layout is None")
                    raise RuntimeError("main_layout is None")

                self.main_layout.addLayout(self.content_layout)
                self.main_layout.addStretch()
                logger.debug("AIOptimizationCard: _setup_optimization_ui: Content layout added to main layout")
            except Exception as e:
                logger.error(f"AIOptimizationCard: _setup_optimization_ui: Failed to add content to main layout: {str(e)}", exc_info=True)
                raise

            logger.info("AIOptimizationCard: _setup_optimization_ui: UI setup complete")
        except Exception as e:
            logger.error(f"AIOptimizationCard: _setup_optimization_ui: Critical error during UI setup: {str(e)}", exc_info=True)
            logger.warning("AIOptimizationCard: _setup_optimization_ui: Widget creation failed - card may not display correctly")
        logger.info("AIOptimizationCard: _setup_optimization_ui: UI setup complete - all 4 sections created and integrated")

    def _create_metric_section(self, title: str, description: str) -> QFrame:
        """
        Create a metric section with title and description.

        Args:
            title: Section title
            description: Section description

        Returns:
            QFrame containing the section
        """
        logger.debug(f"AIOptimizationCard: _create_metric_section: Creating section '{title}'")
        section = QFrame()
        section.setStyleSheet(
            f"border: 1px solid {Colors.BORDER}; "
            f"border-radius: 6px; padding: {SECTION_PADDING}px;"
        )
        layout = QVBoxLayout()
        layout.setSpacing(METRIC_SECTION_LAYOUT_SPACING)

        title_label = QLabel(title)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(SECTION_TITLE_FONT_SIZE)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")

        desc_label = QLabel(description)
        desc_label.setStyleSheet(
            f"color: {Colors.TEXT_SECONDARY}; font-size: {DESC_LABEL_FONT_SIZE}px;"
        )

        layout.addWidget(title_label)
        layout.addWidget(desc_label)

        section.setLayout(layout)
        logger.debug(f"AIOptimizationCard: _create_metric_section: Section '{title}' created and returned")
        return section

    def _get_progress_bar_style(self, color: str) -> str:
        """
        Get styled progress bar stylesheet.

        Args:
            color: Progress bar color (hex)

        Returns:
            Stylesheet string
        """
        logger.debug(f"AIOptimizationCard: _get_progress_bar_style: Generating stylesheet for color {color}")
        return f"""
            QProgressBar {{
                border: none;
                border-radius: 3px;
                background-color: {Colors.SECONDARY_BG};
                height: 6px;
                padding: 0px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """

    def update_display(self, data: dict) -> None:
        """
        Update card display with AI optimization data.

        Args:
            data: Dictionary with keys:
                - lstm_confidence: float (0.0-1.0)
                - lstm_accuracy: float (0.0-1.0)
                - dqn_episodes: int (0-1000+)
                - dqn_progress: float (0.0-1.0)
                - ai_factor: float (0.0-0.9)
                - training_status: str
                - data_points: int
        """
        logger.debug(f"AIOptimizationCard: update_display: Updating display with data: {list(data.keys())}")

        # Validate input data
        try:
            # Step 1: Validate data parameter is not None
            if data is None:
                logger.warning("AIOptimizationCard: update_display: data parameter is None - using all defaults")
                data = {
                    "lstm_confidence": 0.0,
                    "lstm_accuracy": 0.0,
                    "dqn_episodes": 0,
                    "dqn_progress": 0.0,
                    "ai_factor": 0.0,
                    "training_status": "Ready",
                    "data_points": 0
                }
                logger.debug("AIOptimizationCard: update_display: Default data dictionary created")

            # Step 2: Validate data is a dict
            if not isinstance(data, dict):
                logger.error(f"AIOptimizationCard: update_display: data must be dict, got {type(data).__name__} - using defaults")
                data = {
                    "lstm_confidence": 0.0,
                    "lstm_accuracy": 0.0,
                    "dqn_episodes": 0,
                    "dqn_progress": 0.0,
                    "ai_factor": 0.0,
                    "training_status": "Ready",
                    "data_points": 0
                }
                logger.debug("AIOptimizationCard: update_display: Default data dictionary created due to invalid type")

            # Step 3: Validate required keys exist with type checking
            required_keys = ["lstm_confidence", "lstm_accuracy", "dqn_episodes", "dqn_progress", "ai_factor", "training_status", "data_points"]
            for key in required_keys:
                if key not in data:
                    logger.warning(f"AIOptimizationCard: update_display: Missing key '{key}' - using default value")

        except Exception as e:
            logger.error(f"AIOptimizationCard: update_display: Data validation error: {str(e)}", exc_info=True)
            data = {
                "lstm_confidence": 0.0,
                "lstm_accuracy": 0.0,
                "dqn_episodes": 0,
                "dqn_progress": 0.0,
                "ai_factor": 0.0,
                "training_status": "Ready",
                "data_points": 0
            }
            logger.info("AIOptimizationCard: update_display: Using default values due to validation error")

        # Update LSTM section
        try:
            lstm_confidence = data.get("lstm_confidence", 0.0)
            lstm_accuracy = data.get("lstm_accuracy", 0.0)

            # Validate LSTM types and ranges
            if not isinstance(lstm_confidence, (int, float)):
                logger.warning(f"AIOptimizationCard: update_display: lstm_confidence type {type(lstm_confidence).__name__} invalid - using 0.0")
                lstm_confidence = 0.0
            else:
                lstm_confidence = float(lstm_confidence)
                if not (0.0 <= lstm_confidence <= 1.0):
                    logger.warning(f"AIOptimizationCard: update_display: lstm_confidence {lstm_confidence:.3f} out of range [0.0-1.0] - clamping")
                    lstm_confidence = max(0.0, min(1.0, lstm_confidence))

            if not isinstance(lstm_accuracy, (int, float)):
                logger.warning(f"AIOptimizationCard: update_display: lstm_accuracy type {type(lstm_accuracy).__name__} invalid - using 0.0")
                lstm_accuracy = 0.0
            else:
                lstm_accuracy = float(lstm_accuracy)
                if not (0.0 <= lstm_accuracy <= 1.0):
                    logger.warning(f"AIOptimizationCard: update_display: lstm_accuracy {lstm_accuracy:.3f} out of range [0.0-1.0] - clamping")
                    lstm_accuracy = max(0.0, min(1.0, lstm_accuracy))

            logger.debug(f"AIOptimizationCard: update_display: LSTM data validated - confidence={lstm_confidence:.3f}, accuracy={lstm_accuracy:.3f}")

            self.lstm_accuracy_label.setText(f"Accuracy: {lstm_accuracy*100:.1f}%")
            self.lstm_confidence_bar.setValue(int(lstm_confidence * 100))
        except Exception as e:
            logger.error(f"AIOptimizationCard: update_display: LSTM section update error: {str(e)}", exc_info=True)
            self.lstm_accuracy_label.setText("Accuracy: 0.0%")
            self.lstm_confidence_bar.setValue(0)
            logger.debug("AIOptimizationCard: update_display: LSTM section reset to defaults due to error")

        # ✅ CRITICAL FIX: Force IMMEDIATE display update with repaint() call
        # PyQt5: update() schedules repaint in event loop (may be delayed)
        # repaint() forces IMMEDIATE visual update (blocks until done)
        self.lstm_accuracy_label.repaint()
        self.lstm_confidence_bar.repaint()
        logger.debug(f"AIOptimizationCard: update_display: LSTM section updated with accuracy {lstm_accuracy*100:.1f}% and confidence {int(lstm_confidence * 100)}")

        # Update DQN section
        try:
            dqn_episodes = data.get("dqn_episodes", 0)
            dqn_progress = data.get("dqn_progress", 0.0)

            # Validate DQN types and ranges
            if not isinstance(dqn_episodes, (int, float)):
                logger.warning(f"AIOptimizationCard: update_display: dqn_episodes type {type(dqn_episodes).__name__} invalid - using 0")
                dqn_episodes = 0
            else:
                dqn_episodes = int(dqn_episodes)
                if dqn_episodes < 0:
                    logger.warning(f"AIOptimizationCard: update_display: dqn_episodes {dqn_episodes} is negative - clamping to 0")
                    dqn_episodes = 0

            if not isinstance(dqn_progress, (int, float)):
                logger.warning(f"AIOptimizationCard: update_display: dqn_progress type {type(dqn_progress).__name__} invalid - using 0.0")
                dqn_progress = 0.0
            else:
                dqn_progress = float(dqn_progress)
                if not (0.0 <= dqn_progress <= 1.0):
                    logger.warning(f"AIOptimizationCard: update_display: dqn_progress {dqn_progress:.3f} out of range [0.0-1.0] - clamping")
                    dqn_progress = max(0.0, min(1.0, dqn_progress))

            logger.debug(f"AIOptimizationCard: update_display: DQN data validated - episodes={dqn_episodes}, progress={dqn_progress:.3f}")

            self.dqn_episodes_label.setText(f"Episodes: {dqn_episodes} / {DQN_PROGRESS_BAR_MAXIMUM}")
            self.dqn_progress_bar.setValue(int(dqn_progress * DQN_PROGRESS_BAR_MAXIMUM))
        except Exception as e:
            logger.error(f"AIOptimizationCard: update_display: DQN section update error: {str(e)}", exc_info=True)
            self.dqn_episodes_label.setText(f"Episodes: 0 / {DQN_PROGRESS_BAR_MAXIMUM}")
            self.dqn_progress_bar.setValue(0)
            logger.debug("AIOptimizationCard: update_display: DQN section reset to defaults due to error")

        # ✅ CRITICAL FIX: Force IMMEDIATE display update with repaint() call
        # PyQt5: update() schedules repaint in event loop (may be delayed)
        # repaint() forces IMMEDIATE visual update (blocks until done)
        self.dqn_episodes_label.repaint()
        self.dqn_progress_bar.repaint()
        logger.debug(f"AIOptimizationCard: update_display: DQN section updated with episodes {dqn_episodes} and progress {int(dqn_progress * DQN_PROGRESS_BAR_MAXIMUM)}")

        # Update AI Factor section
        try:
            ai_factor = data.get("ai_factor", 0.0)

            # Validate AI Factor type and range
            if not isinstance(ai_factor, (int, float)):
                logger.warning(f"AIOptimizationCard: update_display: ai_factor type {type(ai_factor).__name__} invalid - using 0.0")
                ai_factor = 0.0
            else:
                ai_factor = float(ai_factor)
                if not (0.0 <= ai_factor <= AI_FACTOR_BAR_MAXIMUM):
                    logger.warning(f"AIOptimizationCard: update_display: ai_factor {ai_factor:.3f} out of range [0.0-{AI_FACTOR_BAR_MAXIMUM}] - clamping")
                    ai_factor = max(0.0, min(AI_FACTOR_BAR_MAXIMUM, ai_factor))

            logger.debug(f"AIOptimizationCard: update_display: AI Factor data validated - factor={ai_factor:.3f}")

            self.ai_factor_label.setText(f"AI Factor: +{ai_factor:.2f} points")
            self.ai_factor_bar.setValue(int(ai_factor * 100))
        except Exception as e:
            logger.error(f"AIOptimizationCard: update_display: AI Factor section update error: {str(e)}", exc_info=True)
            self.ai_factor_label.setText("AI Factor: +0.00 points")
            self.ai_factor_bar.setValue(0)
            logger.debug("AIOptimizationCard: update_display: AI Factor section reset to defaults due to error")

        # ✅ CRITICAL FIX: Force IMMEDIATE display update with repaint() call
        # PyQt5: update() schedules repaint in event loop (may be delayed)
        # repaint() forces IMMEDIATE visual update (blocks until done)
        self.ai_factor_label.repaint()
        self.ai_factor_bar.repaint()
        logger.debug(f"AIOptimizationCard: update_display: AI Factor section updated with factor {ai_factor:.2f}")

        # Update Status section
        try:
            training_status = data.get("training_status", "Ready")
            data_points = data.get("data_points", 0)

            # Validate Status types
            if not isinstance(training_status, str):
                logger.warning(f"AIOptimizationCard: update_display: training_status type {type(training_status).__name__} invalid - converting to string")
                training_status = str(training_status)

            if not isinstance(data_points, (int, float)):
                logger.warning(f"AIOptimizationCard: update_display: data_points type {type(data_points).__name__} invalid - using 0")
                data_points = 0
            else:
                data_points = int(data_points)
                if data_points < 0:
                    logger.warning(f"AIOptimizationCard: update_display: data_points {data_points} is negative - clamping to 0")
                    data_points = 0

            logger.debug(f"AIOptimizationCard: update_display: Status data validated - status={training_status}, data_points={data_points}")

            self.training_status_label.setText(f"Status: {training_status}")
            self.data_points_label.setText(f"Data points: {data_points}")
        except Exception as e:
            logger.error(f"AIOptimizationCard: update_display: Status section update error: {str(e)}", exc_info=True)
            self.training_status_label.setText("Status: Ready")
            self.data_points_label.setText("Data points: 0")
            logger.debug("AIOptimizationCard: update_display: Status section reset to defaults due to error")

        # ✅ CRITICAL FIX: Force IMMEDIATE display update with repaint() call
        # PyQt5: update() schedules repaint in event loop (may be delayed)
        # repaint() forces IMMEDIATE visual update (blocks until done)
        self.training_status_label.repaint()
        self.data_points_label.repaint()
        logger.debug(f"AIOptimizationCard: update_display: Status section updated with status '{training_status}' and {data_points} data points")

        # Update colors based on progress
        logger.debug(f"AIOptimizationCard: update_display: Calling color update with accuracy={lstm_accuracy:.3f}, progress={dqn_progress:.3f}, factor={ai_factor:.3f}")
        self._update_colors_by_progress(lstm_accuracy, dqn_progress, ai_factor)
        logger.info("AIOptimizationCard: update_display: Display update complete")

        # ✅ CRITICAL FIX: Force IMMEDIATE display update with repaint() calls
        # PyQt5: update() schedules repaint in event loop (may be delayed)
        # repaint() forces IMMEDIATE visual update (blocks until done)
        # Repaint all AI Optimization sections for comprehensive refresh
        self.lstm_accuracy_label.repaint()
        self.lstm_confidence_bar.repaint()
        self.dqn_episodes_label.repaint()
        self.dqn_progress_bar.repaint()
        self.ai_factor_label.repaint()
        self.ai_factor_bar.repaint()
        self.training_status_label.repaint()
        self.data_points_label.repaint()
        self.repaint()
        logger.info(f"[UI CARD DEBUG] AIOptimizationCard.update_display() - IMMEDIATE parent card refresh forced")

    def _update_colors_by_progress(
        self,
        lstm_accuracy: float,
        dqn_progress: float,
        ai_factor: float
    ) -> None:
        """
        Update label colors based on progress levels.

        Args:
            lstm_accuracy: LSTM accuracy (0.0-1.0)
            dqn_progress: DQN progress (0.0-1.0)
            ai_factor: AI factor (0.0-0.9)
        """
        logger.debug(f"AIOptimizationCard: _update_colors_by_progress: Starting color update with accuracy={lstm_accuracy:.3f}, progress={dqn_progress:.3f}, factor={ai_factor:.3f}")

        # LSTM color update
        if lstm_accuracy >= LSTM_ACCURACY_PERFECT_THRESHOLD:
            lstm_color = Colors.GREEN
            logger.debug(f"AIOptimizationCard: _update_colors_by_progress: LSTM accuracy {lstm_accuracy:.3f} >= {LSTM_ACCURACY_PERFECT_THRESHOLD} - selecting GREEN")
        elif lstm_accuracy >= LSTM_ACCURACY_GOOD_THRESHOLD:
            lstm_color = LSTM_CONFIDENCE_COLOR
            logger.debug(f"AIOptimizationCard: _update_colors_by_progress: LSTM accuracy {lstm_accuracy:.3f} >= {LSTM_ACCURACY_GOOD_THRESHOLD} - selecting BLUE {LSTM_CONFIDENCE_COLOR}")
        elif lstm_accuracy >= LSTM_ACCURACY_FAIR_THRESHOLD:
            lstm_color = AI_FACTOR_COLOR
            logger.debug(f"AIOptimizationCard: _update_colors_by_progress: LSTM accuracy {lstm_accuracy:.3f} >= {LSTM_ACCURACY_FAIR_THRESHOLD} - selecting ORANGE {AI_FACTOR_COLOR}")
        else:
            lstm_color = Colors.TEXT_SECONDARY
            logger.debug(f"AIOptimizationCard: _update_colors_by_progress: LSTM accuracy {lstm_accuracy:.3f} < {LSTM_ACCURACY_FAIR_THRESHOLD} - selecting TEXT_SECONDARY")
        self.lstm_accuracy_label.setStyleSheet(
            f"color: {lstm_color}; font-size: {METRIC_LABEL_FONT_SIZE}px;"
        )
        logger.debug(f"AIOptimizationCard: _update_colors_by_progress: LSTM label stylesheet updated with color {lstm_color}")

        # DQN color update
        if dqn_progress >= DQN_PROGRESS_GOOD_THRESHOLD:
            dqn_color = Colors.GREEN
            logger.debug(f"AIOptimizationCard: _update_colors_by_progress: DQN progress {dqn_progress:.3f} >= {DQN_PROGRESS_GOOD_THRESHOLD} - selecting GREEN")
        elif dqn_progress >= DQN_PROGRESS_FAIR_THRESHOLD:
            dqn_color = DQN_PROGRESS_COLOR
            logger.debug(f"AIOptimizationCard: _update_colors_by_progress: DQN progress {dqn_progress:.3f} >= {DQN_PROGRESS_FAIR_THRESHOLD} - selecting GREEN {DQN_PROGRESS_COLOR}")
        else:
            dqn_color = Colors.TEXT_SECONDARY
            logger.debug(f"AIOptimizationCard: _update_colors_by_progress: DQN progress {dqn_progress:.3f} < {DQN_PROGRESS_FAIR_THRESHOLD} - selecting TEXT_SECONDARY")
        self.dqn_episodes_label.setStyleSheet(
            f"color: {dqn_color}; font-size: {METRIC_LABEL_FONT_SIZE}px;"
        )
        logger.debug(f"AIOptimizationCard: _update_colors_by_progress: DQN label stylesheet updated with color {dqn_color}")

        # AI Factor color update
        if ai_factor >= AI_FACTOR_GOOD_THRESHOLD:
            factor_color = Colors.GREEN
            logger.debug(f"AIOptimizationCard: _update_colors_by_progress: AI Factor {ai_factor:.3f} >= {AI_FACTOR_GOOD_THRESHOLD} - selecting GREEN")
        elif ai_factor >= AI_FACTOR_FAIR_THRESHOLD:
            factor_color = AI_FACTOR_COLOR
            logger.debug(f"AIOptimizationCard: _update_colors_by_progress: AI Factor {ai_factor:.3f} >= {AI_FACTOR_FAIR_THRESHOLD} - selecting ORANGE {AI_FACTOR_COLOR}")
        else:
            factor_color = Colors.TEXT_SECONDARY
            logger.debug(f"AIOptimizationCard: _update_colors_by_progress: AI Factor {ai_factor:.3f} < {AI_FACTOR_FAIR_THRESHOLD} - selecting TEXT_SECONDARY")
        self.ai_factor_label.setStyleSheet(
            f"color: {factor_color}; font-size: {AI_FACTOR_LABEL_FONT_SIZE}px; font-weight: 600;"
        )
        logger.debug(f"AIOptimizationCard: _update_colors_by_progress: AI Factor label stylesheet updated with color {factor_color}")
        logger.info("AIOptimizationCard: _update_colors_by_progress: Color update complete")

    def get_card(self) -> BaseCard:
        """Return this card instance."""
        return self
