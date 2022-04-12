package com.sinlessgamesllc.web.rest;

import static com.sinlessgamesllc.web.rest.TestUtil.sameNumber;
import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.hasItem;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import com.sinlessgamesllc.IntegrationTest;
import com.sinlessgamesllc.domain.Deals;
import com.sinlessgamesllc.repository.DealsRepository;
import java.math.BigDecimal;
import java.util.List;
import java.util.Random;
import java.util.concurrent.atomic.AtomicLong;
import javax.persistence.EntityManager;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.Base64Utils;

/**
 * Integration tests for the {@link DealsResource} REST controller.
 */
@IntegrationTest
@AutoConfigureMockMvc
@WithMockUser
class DealsResourceIT {

    private static final String DEFAULT_NAME = "AAAAAAAAAA";
    private static final String UPDATED_NAME = "BBBBBBBBBB";

    private static final BigDecimal DEFAULT_PRICE = new BigDecimal(1);
    private static final BigDecimal UPDATED_PRICE = new BigDecimal(2);

    private static final String DEFAULT_DESCRIPTION = "AAAAAAAAAA";
    private static final String UPDATED_DESCRIPTION = "BBBBBBBBBB";

    private static final byte[] DEFAULT_IMAGE = TestUtil.createByteArray(1, "0");
    private static final byte[] UPDATED_IMAGE = TestUtil.createByteArray(1, "1");
    private static final String DEFAULT_IMAGE_CONTENT_TYPE = "image/jpg";
    private static final String UPDATED_IMAGE_CONTENT_TYPE = "image/png";

    private static final String ENTITY_API_URL = "/api/deals";
    private static final String ENTITY_API_URL_ID = ENTITY_API_URL + "/{id}";

    private static Random random = new Random();
    private static AtomicLong count = new AtomicLong(random.nextInt() + (2 * Integer.MAX_VALUE));

    @Autowired
    private DealsRepository dealsRepository;

    @Autowired
    private EntityManager em;

    @Autowired
    private MockMvc restDealsMockMvc;

    private Deals deals;

    /**
     * Create an entity for this test.
     *
     * This is a static method, as tests for other entities might also need it,
     * if they test an entity which requires the current entity.
     */
    public static Deals createEntity(EntityManager em) {
        Deals deals = new Deals()
            .name(DEFAULT_NAME)
            .price(DEFAULT_PRICE)
            .description(DEFAULT_DESCRIPTION)
            .image(DEFAULT_IMAGE)
            .imageContentType(DEFAULT_IMAGE_CONTENT_TYPE);
        return deals;
    }

    /**
     * Create an updated entity for this test.
     *
     * This is a static method, as tests for other entities might also need it,
     * if they test an entity which requires the current entity.
     */
    public static Deals createUpdatedEntity(EntityManager em) {
        Deals deals = new Deals()
            .name(UPDATED_NAME)
            .price(UPDATED_PRICE)
            .description(UPDATED_DESCRIPTION)
            .image(UPDATED_IMAGE)
            .imageContentType(UPDATED_IMAGE_CONTENT_TYPE);
        return deals;
    }

    @BeforeEach
    public void initTest() {
        deals = createEntity(em);
    }

    @Test
    @Transactional
    void createDeals() throws Exception {
        int databaseSizeBeforeCreate = dealsRepository.findAll().size();
        // Create the Deals
        restDealsMockMvc
            .perform(post(ENTITY_API_URL).contentType(MediaType.APPLICATION_JSON).content(TestUtil.convertObjectToJsonBytes(deals)))
            .andExpect(status().isCreated());

        // Validate the Deals in the database
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeCreate + 1);
        Deals testDeals = dealsList.get(dealsList.size() - 1);
        assertThat(testDeals.getName()).isEqualTo(DEFAULT_NAME);
        assertThat(testDeals.getPrice()).isEqualByComparingTo(DEFAULT_PRICE);
        assertThat(testDeals.getDescription()).isEqualTo(DEFAULT_DESCRIPTION);
        assertThat(testDeals.getImage()).isEqualTo(DEFAULT_IMAGE);
        assertThat(testDeals.getImageContentType()).isEqualTo(DEFAULT_IMAGE_CONTENT_TYPE);
    }

    @Test
    @Transactional
    void createDealsWithExistingId() throws Exception {
        // Create the Deals with an existing ID
        deals.setId(1L);

        int databaseSizeBeforeCreate = dealsRepository.findAll().size();

        // An entity with an existing ID cannot be created, so this API call must fail
        restDealsMockMvc
            .perform(post(ENTITY_API_URL).contentType(MediaType.APPLICATION_JSON).content(TestUtil.convertObjectToJsonBytes(deals)))
            .andExpect(status().isBadRequest());

        // Validate the Deals in the database
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeCreate);
    }

    @Test
    @Transactional
    void checkNameIsRequired() throws Exception {
        int databaseSizeBeforeTest = dealsRepository.findAll().size();
        // set the field null
        deals.setName(null);

        // Create the Deals, which fails.

        restDealsMockMvc
            .perform(post(ENTITY_API_URL).contentType(MediaType.APPLICATION_JSON).content(TestUtil.convertObjectToJsonBytes(deals)))
            .andExpect(status().isBadRequest());

        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeTest);
    }

    @Test
    @Transactional
    void checkPriceIsRequired() throws Exception {
        int databaseSizeBeforeTest = dealsRepository.findAll().size();
        // set the field null
        deals.setPrice(null);

        // Create the Deals, which fails.

        restDealsMockMvc
            .perform(post(ENTITY_API_URL).contentType(MediaType.APPLICATION_JSON).content(TestUtil.convertObjectToJsonBytes(deals)))
            .andExpect(status().isBadRequest());

        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeTest);
    }

    @Test
    @Transactional
    void checkDescriptionIsRequired() throws Exception {
        int databaseSizeBeforeTest = dealsRepository.findAll().size();
        // set the field null
        deals.setDescription(null);

        // Create the Deals, which fails.

        restDealsMockMvc
            .perform(post(ENTITY_API_URL).contentType(MediaType.APPLICATION_JSON).content(TestUtil.convertObjectToJsonBytes(deals)))
            .andExpect(status().isBadRequest());

        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeTest);
    }

    @Test
    @Transactional
    void getAllDeals() throws Exception {
        // Initialize the database
        dealsRepository.saveAndFlush(deals);

        // Get all the dealsList
        restDealsMockMvc
            .perform(get(ENTITY_API_URL + "?sort=id,desc"))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON_VALUE))
            .andExpect(jsonPath("$.[*].id").value(hasItem(deals.getId().intValue())))
            .andExpect(jsonPath("$.[*].name").value(hasItem(DEFAULT_NAME)))
            .andExpect(jsonPath("$.[*].price").value(hasItem(sameNumber(DEFAULT_PRICE))))
            .andExpect(jsonPath("$.[*].description").value(hasItem(DEFAULT_DESCRIPTION)))
            .andExpect(jsonPath("$.[*].imageContentType").value(hasItem(DEFAULT_IMAGE_CONTENT_TYPE)))
            .andExpect(jsonPath("$.[*].image").value(hasItem(Base64Utils.encodeToString(DEFAULT_IMAGE))));
    }

    @Test
    @Transactional
    void getDeals() throws Exception {
        // Initialize the database
        dealsRepository.saveAndFlush(deals);

        // Get the deals
        restDealsMockMvc
            .perform(get(ENTITY_API_URL_ID, deals.getId()))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON_VALUE))
            .andExpect(jsonPath("$.id").value(deals.getId().intValue()))
            .andExpect(jsonPath("$.name").value(DEFAULT_NAME))
            .andExpect(jsonPath("$.price").value(sameNumber(DEFAULT_PRICE)))
            .andExpect(jsonPath("$.description").value(DEFAULT_DESCRIPTION))
            .andExpect(jsonPath("$.imageContentType").value(DEFAULT_IMAGE_CONTENT_TYPE))
            .andExpect(jsonPath("$.image").value(Base64Utils.encodeToString(DEFAULT_IMAGE)));
    }

    @Test
    @Transactional
    void getNonExistingDeals() throws Exception {
        // Get the deals
        restDealsMockMvc.perform(get(ENTITY_API_URL_ID, Long.MAX_VALUE)).andExpect(status().isNotFound());
    }

    @Test
    @Transactional
    void putNewDeals() throws Exception {
        // Initialize the database
        dealsRepository.saveAndFlush(deals);

        int databaseSizeBeforeUpdate = dealsRepository.findAll().size();

        // Update the deals
        Deals updatedDeals = dealsRepository.findById(deals.getId()).get();
        // Disconnect from session so that the updates on updatedDeals are not directly saved in db
        em.detach(updatedDeals);
        updatedDeals
            .name(UPDATED_NAME)
            .price(UPDATED_PRICE)
            .description(UPDATED_DESCRIPTION)
            .image(UPDATED_IMAGE)
            .imageContentType(UPDATED_IMAGE_CONTENT_TYPE);

        restDealsMockMvc
            .perform(
                put(ENTITY_API_URL_ID, updatedDeals.getId())
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(TestUtil.convertObjectToJsonBytes(updatedDeals))
            )
            .andExpect(status().isOk());

        // Validate the Deals in the database
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeUpdate);
        Deals testDeals = dealsList.get(dealsList.size() - 1);
        assertThat(testDeals.getName()).isEqualTo(UPDATED_NAME);
        assertThat(testDeals.getPrice()).isEqualByComparingTo(UPDATED_PRICE);
        assertThat(testDeals.getDescription()).isEqualTo(UPDATED_DESCRIPTION);
        assertThat(testDeals.getImage()).isEqualTo(UPDATED_IMAGE);
        assertThat(testDeals.getImageContentType()).isEqualTo(UPDATED_IMAGE_CONTENT_TYPE);
    }

    @Test
    @Transactional
    void putNonExistingDeals() throws Exception {
        int databaseSizeBeforeUpdate = dealsRepository.findAll().size();
        deals.setId(count.incrementAndGet());

        // If the entity doesn't have an ID, it will throw BadRequestAlertException
        restDealsMockMvc
            .perform(
                put(ENTITY_API_URL_ID, deals.getId())
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(TestUtil.convertObjectToJsonBytes(deals))
            )
            .andExpect(status().isBadRequest());

        // Validate the Deals in the database
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void putWithIdMismatchDeals() throws Exception {
        int databaseSizeBeforeUpdate = dealsRepository.findAll().size();
        deals.setId(count.incrementAndGet());

        // If url ID doesn't match entity ID, it will throw BadRequestAlertException
        restDealsMockMvc
            .perform(
                put(ENTITY_API_URL_ID, count.incrementAndGet())
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(TestUtil.convertObjectToJsonBytes(deals))
            )
            .andExpect(status().isBadRequest());

        // Validate the Deals in the database
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void putWithMissingIdPathParamDeals() throws Exception {
        int databaseSizeBeforeUpdate = dealsRepository.findAll().size();
        deals.setId(count.incrementAndGet());

        // If url ID doesn't match entity ID, it will throw BadRequestAlertException
        restDealsMockMvc
            .perform(put(ENTITY_API_URL).contentType(MediaType.APPLICATION_JSON).content(TestUtil.convertObjectToJsonBytes(deals)))
            .andExpect(status().isMethodNotAllowed());

        // Validate the Deals in the database
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void partialUpdateDealsWithPatch() throws Exception {
        // Initialize the database
        dealsRepository.saveAndFlush(deals);

        int databaseSizeBeforeUpdate = dealsRepository.findAll().size();

        // Update the deals using partial update
        Deals partialUpdatedDeals = new Deals();
        partialUpdatedDeals.setId(deals.getId());

        partialUpdatedDeals
            .name(UPDATED_NAME)
            .description(UPDATED_DESCRIPTION)
            .image(UPDATED_IMAGE)
            .imageContentType(UPDATED_IMAGE_CONTENT_TYPE);

        restDealsMockMvc
            .perform(
                patch(ENTITY_API_URL_ID, partialUpdatedDeals.getId())
                    .contentType("application/merge-patch+json")
                    .content(TestUtil.convertObjectToJsonBytes(partialUpdatedDeals))
            )
            .andExpect(status().isOk());

        // Validate the Deals in the database
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeUpdate);
        Deals testDeals = dealsList.get(dealsList.size() - 1);
        assertThat(testDeals.getName()).isEqualTo(UPDATED_NAME);
        assertThat(testDeals.getPrice()).isEqualByComparingTo(DEFAULT_PRICE);
        assertThat(testDeals.getDescription()).isEqualTo(UPDATED_DESCRIPTION);
        assertThat(testDeals.getImage()).isEqualTo(UPDATED_IMAGE);
        assertThat(testDeals.getImageContentType()).isEqualTo(UPDATED_IMAGE_CONTENT_TYPE);
    }

    @Test
    @Transactional
    void fullUpdateDealsWithPatch() throws Exception {
        // Initialize the database
        dealsRepository.saveAndFlush(deals);

        int databaseSizeBeforeUpdate = dealsRepository.findAll().size();

        // Update the deals using partial update
        Deals partialUpdatedDeals = new Deals();
        partialUpdatedDeals.setId(deals.getId());

        partialUpdatedDeals
            .name(UPDATED_NAME)
            .price(UPDATED_PRICE)
            .description(UPDATED_DESCRIPTION)
            .image(UPDATED_IMAGE)
            .imageContentType(UPDATED_IMAGE_CONTENT_TYPE);

        restDealsMockMvc
            .perform(
                patch(ENTITY_API_URL_ID, partialUpdatedDeals.getId())
                    .contentType("application/merge-patch+json")
                    .content(TestUtil.convertObjectToJsonBytes(partialUpdatedDeals))
            )
            .andExpect(status().isOk());

        // Validate the Deals in the database
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeUpdate);
        Deals testDeals = dealsList.get(dealsList.size() - 1);
        assertThat(testDeals.getName()).isEqualTo(UPDATED_NAME);
        assertThat(testDeals.getPrice()).isEqualByComparingTo(UPDATED_PRICE);
        assertThat(testDeals.getDescription()).isEqualTo(UPDATED_DESCRIPTION);
        assertThat(testDeals.getImage()).isEqualTo(UPDATED_IMAGE);
        assertThat(testDeals.getImageContentType()).isEqualTo(UPDATED_IMAGE_CONTENT_TYPE);
    }

    @Test
    @Transactional
    void patchNonExistingDeals() throws Exception {
        int databaseSizeBeforeUpdate = dealsRepository.findAll().size();
        deals.setId(count.incrementAndGet());

        // If the entity doesn't have an ID, it will throw BadRequestAlertException
        restDealsMockMvc
            .perform(
                patch(ENTITY_API_URL_ID, deals.getId())
                    .contentType("application/merge-patch+json")
                    .content(TestUtil.convertObjectToJsonBytes(deals))
            )
            .andExpect(status().isBadRequest());

        // Validate the Deals in the database
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void patchWithIdMismatchDeals() throws Exception {
        int databaseSizeBeforeUpdate = dealsRepository.findAll().size();
        deals.setId(count.incrementAndGet());

        // If url ID doesn't match entity ID, it will throw BadRequestAlertException
        restDealsMockMvc
            .perform(
                patch(ENTITY_API_URL_ID, count.incrementAndGet())
                    .contentType("application/merge-patch+json")
                    .content(TestUtil.convertObjectToJsonBytes(deals))
            )
            .andExpect(status().isBadRequest());

        // Validate the Deals in the database
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void patchWithMissingIdPathParamDeals() throws Exception {
        int databaseSizeBeforeUpdate = dealsRepository.findAll().size();
        deals.setId(count.incrementAndGet());

        // If url ID doesn't match entity ID, it will throw BadRequestAlertException
        restDealsMockMvc
            .perform(patch(ENTITY_API_URL).contentType("application/merge-patch+json").content(TestUtil.convertObjectToJsonBytes(deals)))
            .andExpect(status().isMethodNotAllowed());

        // Validate the Deals in the database
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void deleteDeals() throws Exception {
        // Initialize the database
        dealsRepository.saveAndFlush(deals);

        int databaseSizeBeforeDelete = dealsRepository.findAll().size();

        // Delete the deals
        restDealsMockMvc
            .perform(delete(ENTITY_API_URL_ID, deals.getId()).accept(MediaType.APPLICATION_JSON))
            .andExpect(status().isNoContent());

        // Validate the database contains one less item
        List<Deals> dealsList = dealsRepository.findAll();
        assertThat(dealsList).hasSize(databaseSizeBeforeDelete - 1);
    }
}
